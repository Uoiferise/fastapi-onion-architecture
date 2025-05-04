
from typing import TYPE_CHECKING, Any

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import UserModel
from src.schemas.user import UserDB
from src.utils.custom_types import AsyncFunc
from src.utils.repository import SqlAlchemyRepository
from tests import fixtures
from tests.utils import compare_dicts_and_db_models

if TYPE_CHECKING:
    from collections.abc import Sequence


class TestSqlAlchemyRepository:
    class _SqlAlchemyRepository(SqlAlchemyRepository):
        _model = UserModel

    def __get_sql_rep(self, session: AsyncSession) -> SqlAlchemyRepository:
        return self._SqlAlchemyRepository(session)

    @pytest.mark.usefixtures('setup_companies')
    async def test_add_one(
        self,
        transaction_session: AsyncSession,
        first_user: dict,
        get_users: AsyncFunc,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        await sql_rep.add_one(**first_user)
        await transaction_session.flush()

        users_in_db: Sequence[UserModel] = await get_users()
        assert compare_dicts_and_db_models(users_in_db, [first_user], UserDB)

    @pytest.mark.usefixtures('setup_companies')
    async def test_add_one_and_get_id(
        self,
        transaction_session: AsyncSession,
        first_user: dict,
        get_users: AsyncFunc,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        user_id = await sql_rep.add_one_and_get_id(**first_user)
        assert user_id == first_user.get('id')
        await transaction_session.flush()

        users_in_db: Sequence[UserModel] = await get_users()
        assert compare_dicts_and_db_models(users_in_db, [first_user], UserDB)

    @pytest.mark.usefixtures('setup_companies')
    async def test_add_one_and_get_obj(
        self,
        transaction_session: AsyncSession,
        first_user: dict,
        get_users: AsyncFunc,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        user = await sql_rep.add_one_and_get_obj(**first_user)
        assert user.id == first_user.get('id')
        await transaction_session.flush()

        users_in_db: Sequence[UserModel] = await get_users()
        assert compare_dicts_and_db_models(users_in_db, [first_user], UserDB)

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize(
        ('values', 'expected_result', 'expectation'),
        fixtures.test_cases.PARAMS_TEST_SQLALCHEMY_REPOSITORY_GET_BY_QUERY_ONE_OR_NONE,
    )
    async def test_get_by_filter_one_or_none(
        self,
        values: dict,
        expected_result: UserDB,
        expectation: Any,
        transaction_session: AsyncSession,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        with expectation:
            user_in_db: UserModel | None = await sql_rep.get_by_filter_one_or_none(**values)
            result = None if not user_in_db else user_in_db.to_schema()
            assert result == expected_result

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize(
        ('values', 'expected_result', 'expectation'),
        fixtures.test_cases.PARAMS_TEST_SQLALCHEMY_REPOSITORY_GET_BY_QUERY_ALL,
    )
    async def test_get_by_filter_all(
        self,
        values: dict,
        expected_result: list,
        expectation: Any,
        transaction_session: AsyncSession,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        with expectation:
            users_in_db: Sequence[UserModel] = await sql_rep.get_by_filter_all(**values)
            assert compare_dicts_and_db_models(users_in_db, expected_result, UserDB)

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize(
        ('values', 'expected_result', 'expectation'),
        fixtures.test_cases.PARAMS_TEST_SQLALCHEMY_REPOSITORY_UPDATE_ONE_BY_ID,
    )
    async def test_update_one_by_id(
        self,
        values: dict,
        expected_result: UserDB,
        expectation: Any,
        transaction_session: AsyncSession,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        with expectation:
            updated_user: UserModel | None = await sql_rep.update_one_by_id(values.pop('_id'), **values)
            assert updated_user.to_schema() == expected_result

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize(
        ('values', 'expected_result', 'expectation'),
        fixtures.test_cases.PARAMS_TEST_SQLALCHEMY_REPOSITORY_DELETE_BY_QUERY,
    )
    async def test_delete_by_filter(
        self,
        values: dict,
        expected_result: list,
        expectation: Any,
        transaction_session: AsyncSession,
        get_users: AsyncFunc,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        with expectation:
            await sql_rep.delete_by_filter(**values)
            await transaction_session.flush()
            users_in_db: Sequence[UserModel] = await get_users()
            assert compare_dicts_and_db_models(users_in_db, expected_result, UserDB)

    @pytest.mark.usefixtures('setup_users')
    async def test_delete_all(
        self,
        transaction_session: AsyncSession,
        get_users: AsyncFunc,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        await sql_rep.delete_all()
        await transaction_session.flush()
        users_in_db: Sequence[UserModel] = await get_users()
        assert users_in_db == []
