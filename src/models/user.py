from sqlalchemy.orm import Mapped

from src.models import BaseModel
from src.models.mixins.custom_types import created_at_T, str_50_or_none_T, str_50_T, updated_at_T, uuid_pk_T
from src.schemas.user import UserSchema


class UserModel(BaseModel):
    __tablename__ = 'user'

    id: Mapped[uuid_pk_T]
    first_name: Mapped[str_50_T]
    last_name: Mapped[str_50_T]
    middle_name: Mapped[str_50_or_none_T]
    created_at: Mapped[created_at_T]
    updated_at: Mapped[updated_at_T]

    def to_pydantic_schema(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            middle_name=self.middle_name,
        )
