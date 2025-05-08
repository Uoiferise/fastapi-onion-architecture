from uuid import UUID, uuid4

import pytest
from sqlalchemy.exc import MultipleResultsFound

from src.schemas.user import UserDB
from tests.fixtures.db_mocks import USERS
from tests.utils import BaseTestCase

TEST_BASE_SERVICE_GET_BY_QUERY_ONE_OR_NONE_PARAMS: list[BaseTestCase] = [
    BaseTestCase(
        data={'first_name': 'Elon'},
        expected_data=UserDB(
         first_name='Elon',
         last_name='Musk',
         middle_name=None,
         company_id=UUID('b04e55bd-8431-4edd-8eb4-632099c0ea65'),
         id=UUID('bb929d29-a8ef-4a8e-b998-9998984d8fd6'),
        ),
    ),
    BaseTestCase(
        data={'first_name': 'Liza'},
        expected_data=None,
    ),
    BaseTestCase(
        data={'first_name': 'Ivan'},
        expected_data=None,
        expected_error=pytest.raises(MultipleResultsFound),
    ),
]

TEST_BASE_SERVICE_GET_BY_QUERY_ALL_PARAMS: list[BaseTestCase] = [
    BaseTestCase(data={'first_name': 'Elon'}, expected_data=[USERS[1]]),
    BaseTestCase(data={'first_name': 'Liza'}, expected_data=[]),
    BaseTestCase(data={'first_name': 'Ivan'}, expected_data=[USERS[0], USERS[2], USERS[3]]),
]

TEST_BASE_SERVICE_UPDATE_ONE_BY_ID_PARAMS: list[BaseTestCase] = [
    BaseTestCase(
        data={'_id': USERS[0]['id'], 'first_name': 'Liza'},
        expected_data=UserDB(
            first_name='Liza',
            last_name='Ivanov',
            middle_name='Ivanovich',
            company_id=UUID('b04e55bd-8431-4edd-8eb4-632099c0ea65'),
            id=UUID('3d3e784f-646a-4ad4-979c-dca5dcea2a28'),
        ),
    ),
]

TEST_BASE_SERVICE_DELETE_BY_QUERY_PARAMS: list[BaseTestCase] = [
    BaseTestCase(data={'id': USERS[0]['id']}, expected_data=USERS[1:]),
    BaseTestCase(data={'first_name': 'Ivan'}, expected_data=[USERS[1]]),
    BaseTestCase(data={'id': uuid4()}, expected_data=USERS),
    BaseTestCase(data={}, expected_data=[]),
]
