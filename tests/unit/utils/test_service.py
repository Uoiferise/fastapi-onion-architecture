
from typing import TYPE_CHECKING, Any

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import UserDB
from src.utils.custom_types import AsyncFunc
from tests import fixtures
from tests.fixtures import FakeBaseService
from tests.utils import compare_dicts_and_db_models

if TYPE_CHECKING:
    from collections.abc import Sequence

    from src.models import UserModel


class TestBaseService:
    class _BaseService(FakeBaseService):
        _repo = 'user'

    def __get_service(self, session: AsyncSession) -> FakeBaseService:
        return self._BaseService(session)

    @pytest.mark.usefixtures('setup_companies')
    async def test_add_one(
        self,
        transaction_session: AsyncSession,
        first_user: dict,
        get_users: AsyncFunc,
    ) -> None:
        service = self.__get_service(transaction_session)
        await service.add_one(**first_user)

        users_in_db: Sequence[UserModel] = await get_users()
        assert compare_dicts_and_db_models(users_in_db, [first_user], UserDB)

    @pytest.mark.usefixtures('setup_companies')
    async def test_add_one_and_get_id(
        self,
        transaction_session: AsyncSession,
        first_user: dict,
        get_users: AsyncFunc,
    ) -> None:
        service = self.__get_service(transaction_session)
        user_id = await service.add_one_and_get_id(**first_user)
        assert user_id == first_user.get('id')

        users_in_db: Sequence[UserModel] = await get_users()
        assert compare_dicts_and_db_models(users_in_db, [first_user], UserDB)

    @pytest.mark.usefixtures('setup_companies')
    async def test_add_one_and_get_obj(
        self,
        transaction_session: AsyncSession,
        first_user: dict,
        get_users: AsyncFunc,
    ) -> None:
        service = self.__get_service(transaction_session)
        user = await service.add_one_and_get_obj(**first_user)
        assert user.id == first_user.get('id')

        users_in_db: Sequence[UserModel] = await get_users()
        assert compare_dicts_and_db_models(users_in_db, [first_user], UserDB)

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize(
        ('values', 'expected_result', 'expectation'),
        fixtures.test_cases.PARAMS_TEST_BASE_SERVICE_GET_BY_QUERY_ONE_OR_NONE,
    )
    async def test_get_by_query_one_or_none(
        self,
        values: dict,
        expected_result: UserDB,
        expectation: Any,
        transaction_session: AsyncSession,
    ) -> None:
        service = self.__get_service(transaction_session)
        with expectation:
            user_in_db: UserModel | None = await service.get_by_query_one_or_none(**values)
            result = None if not user_in_db else user_in_db.to_schema()
            assert result == expected_result

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize(
        ('values', 'expected_result', 'expectation'),
        fixtures.test_cases.PARAMS_TEST_BASE_SERVICE_GET_BY_QUERY_ALL,
    )
    async def test_get_by_query_all(
        self,
        values: dict,
        expected_result: list,
        expectation: Any,
        transaction_session: AsyncSession,
    ) -> None:
        service = self.__get_service(transaction_session)
        with expectation:
            users_in_db: Sequence[UserModel] = await service.get_by_query_all(**values)
            assert compare_dicts_and_db_models(users_in_db, expected_result, UserDB)

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize(
        ('values', 'expected_result', 'expectation'),
        fixtures.test_cases.PARAMS_TEST_BASE_SERVICE_UPDATE_ONE_BY_ID,
    )
    async def test_update_one_by_id(
        self,
        values: dict,
        expected_result: UserDB,
        expectation: Any,
        transaction_session: AsyncSession,
    ) -> None:
        service = self.__get_service(transaction_session)
        with expectation:
            updated_user: UserModel | None = await service.update_one_by_id(values.pop('_id'), **values)
            assert updated_user.to_schema() == expected_result

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize(
        ('values', 'expected_result', 'expectation'),
        fixtures.test_cases.PARAMS_TEST_BASE_SERVICE_DELETE_BY_QUERY,
    )
    async def test_delete_by_query(
        self,
        values: dict,
        expected_result: list,
        expectation: Any,
        transaction_session: AsyncSession,
        get_users: AsyncFunc,
    ) -> None:
        service = self.__get_service(transaction_session)
        with expectation:
            await service.delete_by_query(**values)
            users_in_db: Sequence[UserModel] = await get_users()
            assert compare_dicts_and_db_models(users_in_db, expected_result, UserDB)

    @pytest.mark.usefixtures('setup_users')
    async def test_delete_all(
        self,
        transaction_session: AsyncSession,
        get_users: AsyncFunc,
    ) -> None:
        service = self.__get_service(transaction_session)
        await service.delete_all()
        users_in_db: Sequence[UserModel] = await get_users()
        assert users_in_db == []
