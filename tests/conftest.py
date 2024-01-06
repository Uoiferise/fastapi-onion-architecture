import asyncio
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)

from src.config import settings
from src.models import BaseModel
from src.main import app


@pytest.fixture(scope="session")
def async_engine() -> AsyncEngine:
    _async_engine = create_async_engine(
        url=settings.DB_URL,
        echo=False,
        future=True,
        pool_size=50,
        max_overflow=100,
        connect_args={
            "prepared_statement_name_func": lambda: f"__asyncpg_{uuid4()}__",
        },
    )
    return _async_engine


@pytest.fixture(scope="session")
def async_session_maker(async_engine):
    _async_session_maker = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    return _async_session_maker


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_db(async_engine):
    assert settings.MODE == "TEST"
    async with async_engine.begin() as db_conn:
        await db_conn.run_sync(BaseModel.metadata.drop_all)
        await db_conn.run_sync(BaseModel.metadata.create_all)
    yield
    async with async_engine.begin() as db_conn:
        await db_conn.run_sync(BaseModel.metadata.drop_all)


@pytest.fixture(scope="function")
async def async_session(async_session_maker) -> AsyncSession:
    async with async_session_maker() as _async_session:
        yield _async_session


@pytest.fixture(scope="session")
def client() -> TestClient:
    with TestClient(app) as c:
        yield c
