from collections.abc import Sequence
from copy import deepcopy

import pytest
import pytest_asyncio
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import CompanyModel, UserModel
from src.utils.custom_types import AsyncFunc
from tests import fixtures
from tests.utils import bulk_save_models


@pytest_asyncio.fixture
async def setup_companies(transaction_session: AsyncSession, companies: tuple[dict]) -> None:
    """..."""
    await bulk_save_models(transaction_session, CompanyModel, companies)


@pytest_asyncio.fixture
async def setup_users(setup_companies: None, transaction_session: AsyncSession, users: tuple[dict]) -> None:
    """..."""
    await bulk_save_models(transaction_session, UserModel, users)


@pytest_asyncio.fixture
def get_users(transaction_session: AsyncSession) -> AsyncFunc:
    """..."""
    async def _get_users() -> Sequence[UserModel]:
        res: Result = await transaction_session.execute(select(UserModel))
        return res.scalars().all()
    return _get_users


@pytest.fixture
def companies() -> tuple[dict]:
    return deepcopy(fixtures.postgres.COMPANIES)


@pytest.fixture
def users() -> tuple[dict]:
    return deepcopy(fixtures.postgres.USERS)


@pytest.fixture
def first_user() -> dict:
    return deepcopy(fixtures.postgres.USERS[0])
