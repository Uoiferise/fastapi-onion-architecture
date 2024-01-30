from typing import Sequence

import pytest

from src.models import UserModel
from src.utils.unit_of_work import UnitOfWork


class TestUnitOfWork:
    async def test_uow_commit(
        self, clean_users, users, get_users, comparing_two_sequence
    ):
        await clean_users()
        uow = UnitOfWork()
        async with uow:
            for user_schema in users:
                await uow.user.add_one(**user_schema.model_dump())

        users_in_db: Sequence[UserModel] = await get_users()
        assert comparing_two_sequence(
            users, [user.to_pydantic_schema() for user in users_in_db]
        )

    async def test_uow_rollback(self, clean_users, users, get_users):
        await clean_users()
        with pytest.raises(Exception):
            uow = UnitOfWork()
            async with uow:
                for user_schema in users:
                    await uow.user.add_one(**user_schema.model_dump())
                raise Exception

        users_in_db: Sequence[UserModel] = await get_users()
        assert list(users_in_db) == []
