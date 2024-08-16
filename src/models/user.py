from sqlalchemy.orm import Mapped

from src.models import BaseModel
from src.schemas.user import UserDB
from src.utils.custom_types import created_at, string_50, string_50_nullable, updated_at, uuid_pk


class UserModel(BaseModel):
    __tablename__ = 'user'

    id: Mapped[uuid_pk]
    first_name: Mapped[string_50]
    last_name: Mapped[string_50]
    middle_name: Mapped[string_50_nullable]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    def to_pydantic_schema(self) -> UserDB:
        return UserDB(**self.__dict__)
