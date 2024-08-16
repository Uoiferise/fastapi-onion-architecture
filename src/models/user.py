from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.models import BaseModel
from src.models.mixins.company_mixin import CompanyMixin
from src.schemas.user import UserDB
from src.utils.custom_types import created_at, updated_at, uuid_pk


class UserModel(CompanyMixin, BaseModel):
    __tablename__ = 'user'

    _company_back_populates: str | None = 'users'

    id: Mapped[uuid_pk]
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    middle_name: Mapped[str | None] = mapped_column(String(50), default=None)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    def to_pydantic_schema(self) -> UserDB:
        return UserDB(**self.__dict__)
