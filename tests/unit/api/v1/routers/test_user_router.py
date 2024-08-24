"""Contains tests for user routes."""
from typing import Any

import pytest
from httpx import AsyncClient

from tests import fixtures
from tests.utils import prepare_payload


class TestUserRouter:

    @staticmethod
    @pytest.mark.usefixtures('setup_companies')
    @pytest.mark.parametrize(
        ('url', 'json', 'headers', 'expected_status_code', 'expected_payload', 'expectation'),
        fixtures.test_cases.PARAMS_TEST_USER_ROUTE_CREATE,
    )
    async def test_create(
        url: str,
        json: dict,
        headers: dict,
        expected_status_code: int,
        expected_payload: dict,
        expectation: Any,
        async_client: AsyncClient,
    ) -> None:
        with expectation:
            response = await async_client.post(url, json=json, headers=headers)
            assert response.status_code == expected_status_code
            assert prepare_payload(response, ['id']) == expected_payload

    @staticmethod
    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize(
        ('url', 'headers', 'expected_status_code', 'expected_payload', 'expectation'),
        fixtures.test_cases.PARAMS_TEST_USER_ROUTE_GET,
    )
    async def test_get(
        url: str,
        headers: dict,
        expected_status_code: int,
        expected_payload: dict,
        expectation: Any,
        async_client: AsyncClient,
    ) -> None:
        with expectation:
            response = await async_client.get(url, headers=headers)
            assert response.status_code == expected_status_code
            assert prepare_payload(response) == expected_payload
