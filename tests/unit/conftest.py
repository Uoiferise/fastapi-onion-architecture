from copy import deepcopy
from typing import Callable, Sequence

import pytest
from sqlalchemy import text, Result, select, insert

from src.models import UserModel
from src.schemas.user import UserSchema
from tests.fakes import FAKE_USERS


@pytest.fixture(scope="function")
def users() -> list[UserSchema]:
    return deepcopy(FAKE_USERS)


@pytest.fixture(scope="session")
def clean_users(async_session_maker) -> Callable:
    sql = text("TRUNCATE public.user RESTART IDENTITY CASCADE;")

    async def _clean_users():
        async with async_session_maker() as session:
            await session.execute(sql)
            await session.commit()

    return _clean_users


@pytest.fixture(scope="session")
def get_users(async_session_maker) -> Callable:
    async def _get_users() -> Sequence[UserModel]:
        async with async_session_maker() as session:
            res: Result = await session.execute(select(UserModel))
            return res.scalars().all()

    return _get_users


@pytest.fixture(scope="function")
def add_users(async_session_maker, users) -> Callable:
    async def _add_users() -> None:
        async with async_session_maker() as session:
            for user_schema in users:
                await session.execute(
                    insert(UserModel).values(**user_schema.model_dump())
                )
            await session.commit()

    return _add_users


@pytest.fixture(scope="session")
def comparing_two_sequence() -> Callable:
    def _comparing_two_sequence(first: Sequence, second: Sequence) -> bool:
        _equality_len = len(first) == len(second)
        _equality_obj = all([obj in second for obj in first])
        return all([_equality_len, _equality_obj])

    return _comparing_two_sequence
