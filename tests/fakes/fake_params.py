from contextlib import nullcontext as does_not_raise
from uuid import uuid4
from copy import deepcopy

import pytest
from sqlalchemy.exc import MultipleResultsFound

from src.schemas.user import UserSchema
from tests.fakes import FAKE_USERS

# kwargs, expected_result, expectation
TEST_BASE_SERVICE_GET_BY_QUERY_ONE_OR_NONE_PARAMS = [
    ({"first_name": "Elon"}, FAKE_USERS[1], does_not_raise()),
    ({"first_name": "Liza"}, None, does_not_raise()),
    ({"first_name": "Ivan"}, None, pytest.raises(MultipleResultsFound)),
]

# kwargs, expected_result, expectation
TEST_BASE_SERVICE_GET_BY_QUERY_ALL_PARAMS = [
    ({"first_name": "Elon"}, [FAKE_USERS[1]], does_not_raise()),
    ({"first_name": "Liza"}, None, does_not_raise()),
    ({"first_name": "Ivan"}, [FAKE_USERS[0], FAKE_USERS[2]], does_not_raise()),
]

# kwargs, expected_result, expectation
TEST_BASE_SERVICE_UPDATE_ONE_BY_ID_PARAMS = [
    (
        {"_id": FAKE_USERS[0].id, "first_name": "Liza"},
        UserSchema(
            id=FAKE_USERS[0].id,
            first_name="Liza",
            last_name=FAKE_USERS[0].last_name,
            middle_name=FAKE_USERS[0].middle_name,
        ),
        does_not_raise(),
    ),
]

# kwargs, expected_result, expectation
TEST_BASE_SERVICE_DELETE_BY_QUERY_PARAMS = [
    ({"id": FAKE_USERS[0].id}, FAKE_USERS[1:], does_not_raise()),
    ({"first_name": "Ivan"}, [FAKE_USERS[1]], does_not_raise()),
    ({"id": uuid4()}, FAKE_USERS, does_not_raise()),
]

# kwargs, expected_result, expectation
TEST_SQLALCHEMY_REPOSITORY_GET_BY_QUERY_ONE_OR_NONE_PARAMS = deepcopy(
    TEST_BASE_SERVICE_GET_BY_QUERY_ONE_OR_NONE_PARAMS
)

# kwargs, expected_result, expectation
TEST_SQLALCHEMY_REPOSITORY_GET_BY_QUERY_ALL_PARAMS = deepcopy(
    TEST_BASE_SERVICE_GET_BY_QUERY_ALL_PARAMS
)

# kwargs, expected_result, expectation
TEST_SQLALCHEMY_REPOSITORY_UPDATE_ONE_BY_ID_PARAMS = deepcopy(
    TEST_BASE_SERVICE_UPDATE_ONE_BY_ID_PARAMS
)


# kwargs, expected_result, expectation
TEST_SQLALCHEMY_REPOSITORY_DELETE_BY_QUERY_PARAMS = deepcopy(
    TEST_BASE_SERVICE_DELETE_BY_QUERY_PARAMS
)
