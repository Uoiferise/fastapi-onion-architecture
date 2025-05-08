from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from tests.constants import BASE_ENDPOINT_URL
from tests.utils import RequestTestCase

TEST_COMPANY_ROUTE_CREATE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/company/',
        headers={},
        data={
            'inn': 1,
            'company_name': 'Test_name',
        },
        expected_status=HTTP_201_CREATED,
        expected_data={
            'inn': 1,
            'company_name': 'Test_name',
            'is_active': True,
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/company/',
        headers={},
        data={
            'inn': 1,
            'company_name': '1' * 51,
        },
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid request body',
    ),
]

TEST_COMPANY_ROUTE_GET_WITH_USERS_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/company/b04e55bd-8431-4edd-8eb4-632099c0ea65',
        headers={},
        expected_status=HTTP_200_OK,
        expected_data={
            'company_name': 'First Test Company',
            'id': 'b04e55bd-8431-4edd-8eb4-632099c0ea65',
            'inn': 123456789,
            'is_active': True,
            'users': [
                {
                    'company_id': 'b04e55bd-8431-4edd-8eb4-632099c0ea65',
                    'first_name': 'Ivan',
                    'id': '3d3e784f-646a-4ad4-979c-dca5dcea2a28',
                    'last_name': 'Ivanov',
                    'middle_name': 'Ivanovich',
                },
                {
                    'company_id': 'b04e55bd-8431-4edd-8eb4-632099c0ea65',
                    'first_name': 'Elon',
                    'id': 'bb929d29-a8ef-4a8e-b998-9998984d8fd6',
                    'last_name': 'Musk',
                    'middle_name': None,
                },
                {
                    'company_id': 'b04e55bd-8431-4edd-8eb4-632099c0ea65',
                    'first_name': 'Ivan',
                    'id': 'd5621653-f72b-4124-98e6-79c5d9c2dc2b',
                    'last_name': 'Terrible',
                    'middle_name': 'Vasilievich',
                },
            ],
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/company/1',
        headers={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid company id',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/company/a04e55bd-8431-4edd-8eb4-632099c0ea65',
        headers={},
        expected_status=HTTP_404_NOT_FOUND,
        expected_data={},
        description='Non-existent company',
    ),
]
