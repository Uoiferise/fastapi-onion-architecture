from uuid import uuid4

from src.schemas.user import UserDB

FAKE_USERS: list[UserDB] = [
    UserDB(
        id=uuid4(),
        first_name='Ivan',
        last_name='Ivanov',
        middle_name='Ivanovich',
    ),
    UserDB(
        id=uuid4(),
        first_name='Elon',
        last_name='Musk',
        middle_name=None,
    ),
    UserDB(
        id=uuid4(),
        first_name='Ivan',
        last_name='Terrible',
        middle_name='Vasilievich',
    ),
]
