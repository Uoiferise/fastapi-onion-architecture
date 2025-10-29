"""Contains tests for company routes."""

import pytest
from httpx import AsyncClient

from tests.fixtures import testing_cases
from tests.utils import RequestTestCase, prepare_payload


class TestCompanyRouter:

    @staticmethod
    @pytest.mark.parametrize('case', testing_cases.TEST_COMPANY_ROUTE_CREATE_PARAMS)
    async def test_create(
        case: RequestTestCase,
        async_client: AsyncClient,
    ) -> None:
        with case.expected_error:
            response = await async_client.post(case.url, json=case.data, headers=case.headers)
            assert response.status_code == case.expected_status
            assert prepare_payload(response, ['id']) == case.expected_data

    @staticmethod
    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize('case', testing_cases.TEST_COMPANY_ROUTE_GET_WITH_USERS_PARAMS)
    async def test_get_company_with_users(
        case: RequestTestCase,
        async_client: AsyncClient,
    ) -> None:
        with case.expected_error:
            response = await async_client.get(case.url, headers=case.headers)
            assert response.status_code == case.expected_status
            assert prepare_payload(response) == case.expected_data
