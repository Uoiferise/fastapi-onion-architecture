"""Contains helper fixtures for setup tests infrastructure."""

import asyncio
from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
import sqlalchemy
from httpx import AsyncClient
from sqlalchemy import Result, sql
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from src.config import settings
from src.main import app
from src.models import BaseModel
from src.services import CompanyService, UserService
from tests.fixtures import FakeCompanyService, FakeUserService


@pytest.fixture(scope='session')
def event_loop(request: pytest.FixtureRequest) -> asyncio.AbstractEventLoop:
    """Returns a new event_loop."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def create_test_db(event_loop: None) -> None:
    """Creates a test base for the duration of the tests."""
    assert settings.MODE == 'TEST'

    sqlalchemy_database_url = (
        f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}'
        f'@{settings.DB_HOST}:{settings.DB_PORT}/'
    )
    nodb_engine = create_async_engine(
        sqlalchemy_database_url,
        echo=False,
        future=True,
    )
    db = AsyncSession(bind=nodb_engine)

    db_exists_query = sql.text(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{settings.DB_NAME}'")
    db_exists: Result = await db.execute(db_exists_query)
    db_exists = db_exists.fetchone() is not None
    autocommit_engine = nodb_engine.execution_options(isolation_level='AUTOCOMMIT')
    connection = await autocommit_engine.connect()
    if not db_exists:
        db_create_query = sql.text(f'CREATE DATABASE {settings.DB_NAME}')
        await connection.execute(db_create_query)

    yield

    db_drop_query = sql.text(f'DROP DATABASE IF EXISTS {settings.DB_NAME} WITH (FORCE)')
    await db.close()
    await connection.execute(db_drop_query)
    await connection.close()
    await nodb_engine.dispose()


@pytest_asyncio.fixture(scope='session')
async def db_engine(create_test_db: None) -> AsyncGenerator[AsyncEngine, None]:
    """Returns the test Engine."""
    engine = create_async_engine(
        settings.DB_URL,
        echo=False,
        future=True,
        pool_size=50,
        max_overflow=100,
    ).execution_options(compiled_cache=None)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def setup_schemas(db_engine: AsyncEngine) -> None:
    """Creates schemas in the test database."""
    assert settings.MODE == 'TEST'

    schemas = (
        'schema_for_example',
    )

    async with db_engine.connect() as conn:
        for schema in schemas:
            await conn.execute(sqlalchemy.schema.CreateSchema(schema))
            await conn.commit()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def setup_db(db_engine: AsyncEngine, setup_schemas: None) -> None:
    """Creates tables in the test database and insert needs data."""
    assert settings.MODE == 'TEST'

    async with db_engine.begin() as db_conn:
        await db_conn.run_sync(BaseModel.metadata.drop_all)
        await db_conn.run_sync(BaseModel.metadata.create_all)


@pytest_asyncio.fixture
async def transaction_session(db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Returns a connection to the database.
    Any changes made to the database will NOT be applied, only for the duration of the TestCase.
    """
    connection = await db_engine.connect()
    await connection.begin()
    session = AsyncSession(bind=connection)

    yield session

    await session.rollback()
    await connection.close()


@pytest_asyncio.fixture
def fake_user_service(transaction_session: AsyncSession) -> Generator[FakeUserService, None]:
    """..."""
    _fake_user_service = FakeUserService(transaction_session)
    yield _fake_user_service


@pytest_asyncio.fixture
def fake_company_service(transaction_session: AsyncSession) -> Generator[FakeCompanyService, None]:
    """..."""
    _fake_company_service = FakeCompanyService(transaction_session)
    yield _fake_company_service


@pytest_asyncio.fixture
async def async_client(
    fake_user_service: FakeUserService,
    fake_company_service: FakeCompanyService,
) -> AsyncGenerator[AsyncClient, None]:
    """..."""
    app.dependency_overrides[UserService] = lambda: fake_user_service
    app.dependency_overrides[CompanyService] = lambda: fake_company_service
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
