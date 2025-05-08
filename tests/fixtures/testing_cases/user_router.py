from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from tests.constants import BASE_ENDPOINT_URL
from tests.utils import RequestTestCase

TEST_USER_ROUTE_CREATE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/user/',
        headers={},
        data={
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'middle_name': 'Ivanovich',
            'company_id': 'b04e55bd-8431-4edd-8eb4-632099c0ea65',
        },
        expected_status=HTTP_201_CREATED,
        expected_data={
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'middle_name': 'Ivanovich',
            'company_id': 'b04e55bd-8431-4edd-8eb4-632099c0ea65',
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/user/',
        headers={},
        data={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid request body',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/user/',
        headers={},
        data={
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'middle_name': 'Ivanovich',
            'company_id': '00000000-0000-0000-0000-000000000000',
        },
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Non-existent company',
    ),
]

TEST_USER_ROUTE_GET_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/user/3d3e784f-646a-4ad4-979c-dca5dcea2a28',
        headers={},
        expected_status=HTTP_200_OK,
        expected_data={
            'company_id': 'b04e55bd-8431-4edd-8eb4-632099c0ea65',
            'first_name': 'Ivan',
            'id': '3d3e784f-646a-4ad4-979c-dca5dcea2a28',
            'last_name': 'Ivanov',
            'middle_name': 'Ivanovich',
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/user/1',
        headers={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid user id',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/user/4d3e784f-646a-4ad4-979c-dca5dcea2a28',
        headers={},
        expected_status=HTTP_404_NOT_FOUND,
        expected_data={},
        description='Non-existent user',
    ),
]
