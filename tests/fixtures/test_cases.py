from contextlib import nullcontext as does_not_raise
from copy import deepcopy
from uuid import UUID, uuid4

import pytest
from sqlalchemy.exc import MultipleResultsFound

from src.schemas.user import UserDB
from tests.fixtures.postgres import USERS

# values, expected_result, expectation
PARAMS_TEST_BASE_SERVICE_GET_BY_QUERY_ONE_OR_NONE = [
    ({'first_name': 'Elon'},
     UserDB(
         first_name='Elon',
         last_name='Musk',
         middle_name=None,
         company_id=UUID('b04e55bd-8431-4edd-8eb4-632099c0ea65'),
         id=UUID('bb929d29-a8ef-4a8e-b998-9998984d8fd6'),
     ),
     does_not_raise()),
    ({'first_name': 'Liza'}, None, does_not_raise()),
    ({'first_name': 'Ivan'}, None, pytest.raises(MultipleResultsFound)),
]

# values, expected_result, expectation
PARAMS_TEST_BASE_SERVICE_GET_BY_QUERY_ALL = [
    ({'first_name': 'Elon'}, [USERS[1]], does_not_raise()),
    ({'first_name': 'Liza'}, [], does_not_raise()),
    ({'first_name': 'Ivan'}, [USERS[0], USERS[2], USERS[3]], does_not_raise()),
]

# values, expected_result, expectation
PARAMS_TEST_BASE_SERVICE_UPDATE_ONE_BY_ID = [
    (
        {'_id': USERS[0]['id'], 'first_name': 'Liza'},
        UserDB(
            first_name='Liza',
            last_name='Ivanov',
            middle_name='Ivanovich',
            company_id=UUID('b04e55bd-8431-4edd-8eb4-632099c0ea65'),
            id=UUID('3d3e784f-646a-4ad4-979c-dca5dcea2a28'),
        ),
        does_not_raise(),
    ),
]

# values, expected_result, expectation
PARAMS_TEST_BASE_SERVICE_DELETE_BY_QUERY = [
    ({'id': USERS[0]['id']}, USERS[1:], does_not_raise()),
    ({'first_name': 'Ivan'}, [USERS[1]], does_not_raise()),
    ({'id': uuid4()}, USERS, does_not_raise()),
    ({}, [], does_not_raise()),
]

# values, expected_result, expectation
PARAMS_TEST_SQLALCHEMY_REPOSITORY_GET_BY_QUERY_ONE_OR_NONE = deepcopy(
    PARAMS_TEST_BASE_SERVICE_GET_BY_QUERY_ONE_OR_NONE,
)

# values, expected_result, expectation
PARAMS_TEST_SQLALCHEMY_REPOSITORY_GET_BY_QUERY_ALL = deepcopy(
    PARAMS_TEST_BASE_SERVICE_GET_BY_QUERY_ALL,
)

# values, expected_result, expectation
PARAMS_TEST_SQLALCHEMY_REPOSITORY_UPDATE_ONE_BY_ID = deepcopy(
    PARAMS_TEST_BASE_SERVICE_UPDATE_ONE_BY_ID,
)

# values, expected_result, expectation
PARAMS_TEST_SQLALCHEMY_REPOSITORY_DELETE_BY_QUERY = deepcopy(
    PARAMS_TEST_BASE_SERVICE_DELETE_BY_QUERY,
)

# url, json, headers, expected_status_code, expected_payload, expectation
PARAMS_TEST_USER_ROUTE_CREATE = [
    # positive case
    (
        'api/v1/user/',
        {
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'middle_name': 'Ivanovich',
            'company_id': 'b04e55bd-8431-4edd-8eb4-632099c0ea65',
        }, {}, 201, {
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'middle_name': 'Ivanovich',
            'company_id': 'b04e55bd-8431-4edd-8eb4-632099c0ea65',
        }, does_not_raise(),
    ),
    # not valid request body
    (
        'api/v1/user/',
        {}, {}, 422, {}, does_not_raise(),
    ),
    # non-existent company
    (
        'api/v1/user/',
        {
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'middle_name': 'Ivanovich',
            'company_id': '00000000-0000-0000-0000-000000000000',
        }, {}, 422, {}, does_not_raise(),
    ),
]

# url, headers, expected_status_code, expected_payload, expectation
PARAMS_TEST_USER_ROUTE_GET = [
    # positive case
    (
        'api/v1/user/3d3e784f-646a-4ad4-979c-dca5dcea2a28', {},
        200, {
            'company_id': 'b04e55bd-8431-4edd-8eb4-632099c0ea65',
            'first_name': 'Ivan',
            'id': '3d3e784f-646a-4ad4-979c-dca5dcea2a28',
            'last_name': 'Ivanov',
            'middle_name': 'Ivanovich',
        }, does_not_raise(),
    ),
    # not valid user id
    (
        'api/v1/user/1', {},
        422, {}, does_not_raise(),
    ),
    # non-existent user
    (
        'api/v1/user/4d3e784f-646a-4ad4-979c-dca5dcea2a28', {},
        404, {}, does_not_raise(),
    ),
]

# url, json, headers, expected_status_code, expected_payload, expectation
PARAMS_TEST_COMPANY_ROUTE_CREATE = [
    # positive case
    (
        'api/v1/company/',
        {
            'inn': 1,
            'company_name': 'Test_name',
        }, {}, 201, {
            'inn': 1,
            'company_name': 'Test_name',
            'is_active': True,
        }, does_not_raise(),
    ),
    # not valid request body
    (
        'api/v1/company/',
        {
            'inn': 1,
            'company_name': '1' * 51,
        }, {}, 422, {}, does_not_raise(),
    ),
]

# url, headers, expected_status_code, expected_payload, expectation
PARAMS_TEST_COMPANY_ROUTE_GET_WITH_USERS = [
    # positive case
    (
        'api/v1/company/b04e55bd-8431-4edd-8eb4-632099c0ea65', {},
        200, {
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
        }, does_not_raise(),
    ),
    # not valid company id
    (
        'api/v1/company/1', {},
        422, {}, does_not_raise(),
    ),
    # non-existent company
    (
        'api/v1/company/a04e55bd-8431-4edd-8eb4-632099c0ea65', {},
        404, {}, does_not_raise(),
    ),
]
