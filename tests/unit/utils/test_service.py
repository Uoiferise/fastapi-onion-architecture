from typing import Sequence
from uuid import uuid4

import pytest
from sqlalchemy.engine import Row

from src.models import UserModel
from src.utils.service import BaseService
from src.utils.unit_of_work import UnitOfWork
from tests.fakes import (
    TEST_BASE_SERVICE_GET_BY_QUERY_ONE_OR_NONE_PARAMS,
    TEST_BASE_SERVICE_GET_BY_QUERY_ALL_PARAMS,
    TEST_BASE_SERVICE_UPDATE_ONE_BY_ID_PARAMS,
    TEST_BASE_SERVICE_DELETE_BY_QUERY_PARAMS,
)


class TestBaseService:
    class _BaseService(BaseService):
        base_repository = "user"

    async def test_add_one(self, clean_users, users, get_users, comparing_two_sequence):
        await clean_users()
        for user_schema in users:
            await self._BaseService.add_one(
                uow=UnitOfWork(), **user_schema.model_dump()
            )

        users_in_db: Sequence[UserModel] = await get_users()
        assert comparing_two_sequence(
            users, [user.to_pydantic_schema() for user in users_in_db]
        )

    async def test_add_one_and_get_id(
        self, clean_users, users, get_users, comparing_two_sequence
    ):
        await clean_users()
        for user_schema in users:
            user_id: uuid4 = await self._BaseService.add_one_and_get_id(
                uow=UnitOfWork(), **user_schema.model_dump()
            )
            assert user_schema.id == user_id

        users_in_db: Sequence[UserModel] = await get_users()
        assert comparing_two_sequence(
            users, [user.to_pydantic_schema() for user in users_in_db]
        )

    async def test_add_one_and_get_obj(
        self, clean_users, users, get_users, comparing_two_sequence
    ):
        await clean_users()
        for user_schema in users:
            user_in_db: UserModel = await self._BaseService.add_one_and_get_obj(
                uow=UnitOfWork(), **user_schema.model_dump()
            )
            assert user_schema == user_in_db.to_pydantic_schema()

        users_in_db: Sequence[UserModel] = await get_users()
        assert comparing_two_sequence(
            users, [user.to_pydantic_schema() for user in users_in_db]
        )

    @pytest.mark.parametrize(
        "kwargs, expected_result, expectation",
        TEST_BASE_SERVICE_GET_BY_QUERY_ONE_OR_NONE_PARAMS,
    )
    async def test_get_by_query_one_or_none(
        self, kwargs, expected_result, expectation, clean_users, add_users
    ):
        await clean_users()
        await add_users()

        with expectation:
            user_in_db: UserModel | None = (
                await self._BaseService.get_by_query_one_or_none(
                    uow=UnitOfWork(), **kwargs
                )
            )
            result = None if not user_in_db else user_in_db.to_pydantic_schema()
            assert result == expected_result

    @pytest.mark.parametrize(
        "kwargs, expected_result, expectation",
        TEST_BASE_SERVICE_GET_BY_QUERY_ALL_PARAMS,
    )
    async def test_get_by_query_all(
        self,
        kwargs,
        expected_result,
        expectation,
        clean_users,
        add_users,
        comparing_two_sequence,
    ):
        await clean_users()
        await add_users()

        with expectation:
            users_in_db: Sequence[UserModel] = await self._BaseService.get_by_query_all(
                uow=UnitOfWork(), **kwargs
            )
            result = (
                None
                if not users_in_db
                else [user.to_pydantic_schema() for user in users_in_db]
            )
            if result:
                assert comparing_two_sequence(result, expected_result)
            else:
                assert result == expected_result

    @pytest.mark.parametrize(
        "kwargs, expected_result, expectation",
        TEST_BASE_SERVICE_UPDATE_ONE_BY_ID_PARAMS,
    )
    async def test_update_one_by_id(
        self,
        kwargs,
        expected_result,
        expectation,
        clean_users,
        add_users,
        comparing_two_sequence,
    ):
        await clean_users()
        await add_users()

        with expectation:
            updated_user: UserModel | None = await self._BaseService.update_one_by_id(
                uow=UnitOfWork(), _id=kwargs.pop("_id"), values=kwargs
            )

            assert updated_user.to_pydantic_schema() == expected_result

    @pytest.mark.parametrize(
        "kwargs, expected_result, expectation", TEST_BASE_SERVICE_DELETE_BY_QUERY_PARAMS
    )
    async def test_delete_by_query(
        self,
        kwargs,
        expected_result,
        expectation,
        clean_users,
        add_users,
        get_users,
        comparing_two_sequence,
    ):
        await clean_users()
        await add_users()

        with expectation:
            await self._BaseService.delete_by_query(uow=UnitOfWork(), **kwargs)
            users_in_db: Sequence[UserModel] = await get_users()
            assert comparing_two_sequence(
                expected_result, [user.to_pydantic_schema() for user in users_in_db]
            )

    async def test_delete_all(
        self,
        clean_users,
        get_users,
        add_users,
    ):
        await clean_users()
        await add_users()

        await self._BaseService.delete_all(uow=UnitOfWork())
        chats_in_db: Sequence[UserModel] = await get_users()
        assert chats_in_db == []
