from typing import Sequence
from uuid import uuid4

import pytest
from sqlalchemy import Row

from src.models import UserModel
from src.utils.repository import SqlAlchemyRepository
from tests.fakes import (
    TEST_SQLALCHEMY_REPOSITORY_GET_BY_QUERY_ONE_OR_NONE_PARAMS,
    TEST_SQLALCHEMY_REPOSITORY_GET_BY_QUERY_ALL_PARAMS,
    TEST_SQLALCHEMY_REPOSITORY_UPDATE_ONE_BY_ID_PARAMS,
    TEST_SQLALCHEMY_REPOSITORY_DELETE_BY_QUERY_PARAMS,
)


class TestSqlAlchemyRepository:
    class _SqlAlchemyRepository(SqlAlchemyRepository):
        model = UserModel

    async def test_add_one(
        self, clean_users, users, get_users, comparing_two_sequence, async_session
    ):
        await clean_users()
        sql_alchemy_repository = self._SqlAlchemyRepository(session=async_session)
        for user_schema in users:
            await sql_alchemy_repository.add_one(**user_schema.model_dump())
            await sql_alchemy_repository.session.commit()

        users_in_db: Sequence[UserModel] = await get_users()
        assert comparing_two_sequence(
            users, [user.to_pydantic_schema() for user in users_in_db]
        )
        await async_session.close()

    async def test_add_one_and_get_id(
        self, clean_users, users, get_users, comparing_two_sequence, async_session
    ):
        await clean_users()
        sql_alchemy_repository = self._SqlAlchemyRepository(session=async_session)
        for user_schema in users:
            user_id: uuid4 = await sql_alchemy_repository.add_one_and_get_id(
                **user_schema.model_dump()
            )
            await sql_alchemy_repository.session.commit()
            assert user_schema.id == user_id

        users_in_db: Sequence[UserModel] = await get_users()
        assert comparing_two_sequence(
            users, [user.to_pydantic_schema() for user in users_in_db]
        )
        await async_session.close()

    async def test_add_one_and_get_obj(
        self, clean_users, users, get_users, comparing_two_sequence, async_session
    ):
        await clean_users()
        sql_alchemy_repository = self._SqlAlchemyRepository(session=async_session)
        for user_schema in users:
            user_in_db: UserModel = await sql_alchemy_repository.add_one_and_get_obj(
                **user_schema.model_dump()
            )
            await sql_alchemy_repository.session.commit()
            assert user_schema == user_in_db.to_pydantic_schema()

        users_in_db: Sequence[UserModel] = await get_users()
        assert comparing_two_sequence(
            users, [user.to_pydantic_schema() for user in users_in_db]
        )
        await async_session.close()

    @pytest.mark.parametrize(
        "kwargs, expected_result, expectation",
        TEST_SQLALCHEMY_REPOSITORY_GET_BY_QUERY_ONE_OR_NONE_PARAMS,
    )
    async def test_get_by_query_one_or_none(
        self,
        kwargs,
        expected_result,
        expectation,
        clean_users,
        add_users,
        async_session,
    ):
        await clean_users()
        await add_users()
        sql_alchemy_repository = self._SqlAlchemyRepository(session=async_session)

        with expectation:
            user_in_db: UserModel | None = (
                await sql_alchemy_repository.get_by_query_one_or_none(**kwargs)
            )
            result = None if not user_in_db else user_in_db.to_pydantic_schema()
            assert result == expected_result
        await async_session.close()

    @pytest.mark.parametrize(
        "kwargs, expected_result, expectation",
        TEST_SQLALCHEMY_REPOSITORY_GET_BY_QUERY_ALL_PARAMS,
    )
    async def test_get_by_query_all(
        self,
        kwargs,
        expected_result,
        expectation,
        clean_users,
        add_users,
        comparing_two_sequence,
        async_session,
    ):
        await clean_users()
        await add_users()
        sql_alchemy_repository = self._SqlAlchemyRepository(session=async_session)

        with expectation:
            users_in_db: Sequence[
                UserModel
            ] = await sql_alchemy_repository.get_by_query_all(**kwargs)
            result = (
                None
                if not users_in_db
                else [user.to_pydantic_schema() for user in users_in_db]
            )
            if result:
                assert comparing_two_sequence(result, expected_result)
            else:
                assert result == expected_result
        await async_session.close()

    @pytest.mark.parametrize(
        "kwargs, expected_result, expectation",
        TEST_SQLALCHEMY_REPOSITORY_UPDATE_ONE_BY_ID_PARAMS,
    )
    async def test_update_one_by_id(
        self,
        kwargs,
        expected_result,
        expectation,
        clean_users,
        add_users,
        comparing_two_sequence,
        async_session,
    ):
        await clean_users()
        await add_users()
        sql_alchemy_repository = self._SqlAlchemyRepository(session=async_session)

        with expectation:
            updated_user: UserModel | None = (
                await sql_alchemy_repository.update_one_by_id(
                    _id=kwargs.pop("_id"), values=kwargs
                )
            )
            assert updated_user.to_pydantic_schema() == expected_result
        await async_session.close()

    @pytest.mark.parametrize(
        "kwargs, expected_result, expectation",
        TEST_SQLALCHEMY_REPOSITORY_DELETE_BY_QUERY_PARAMS,
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
        async_session,
    ):
        await clean_users()
        await add_users()
        sql_alchemy_repository = self._SqlAlchemyRepository(session=async_session)
        with expectation:
            await sql_alchemy_repository.delete_by_query(**kwargs)
            await async_session.commit()
            users_in_db: Sequence[UserModel] = await get_users()
            assert comparing_two_sequence(
                expected_result, [user.to_pydantic_schema() for user in users_in_db]
            )
        await async_session.close()

    async def test_delete_all(self, clean_users, get_users, add_users, async_session):
        await clean_users()
        await add_users()
        sql_alchemy_repository = self._SqlAlchemyRepository(session=async_session)
        await sql_alchemy_repository.delete_all()
        await async_session.commit()
        users_in_db: Sequence[UserModel] = await get_users()
        assert users_in_db == []
