from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import Mapped, relationship

from src.models import BaseModel
from src.schemas.company import CompanyDB
from src.utils.custom_types import created_at, updated_at, uuid_pk

if TYPE_CHECKING:
    from src.models.user import UserModel


class CompanyModel(BaseModel):
    __tablename__ = 'company'

    id: Mapped[uuid_pk]
    inn: Mapped[int]
    company_name: Mapped[str] = Column(String(256))
    is_active: Mapped[bool] = Column(Boolean, default=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    users: Mapped[list['UserModel']] = relationship(back_populates='company')

    def to_schema(self) -> CompanyDB:
        return CompanyDB(**self.__dict__)
