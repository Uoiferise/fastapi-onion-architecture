from uuid import uuid4

from src.schemas.user import UserSchema

FAKE_USERS: list[UserSchema] = [
    UserSchema(
        id=uuid4(),
        first_name='Ivan',
        last_name='Ivanov',
        middle_name='Ivanovich',
    ),
    UserSchema(
        id=uuid4(),
        first_name='Elon',
        last_name='Musk',
        middle_name=None,
    ),
    UserSchema(
        id=uuid4(),
        first_name='Ivan',
        last_name='Terrible',
        middle_name='Vasilievich',
    ),
]
