from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

if TYPE_CHECKING:
    from src.models.company import CompanyModel


class CompanyMixin:
    _company_id_nullable: bool = False
    _company_id_unique: bool = False
    _company_back_populates: str | None = None

    @declared_attr
    def company_id(self) -> Mapped[str]:
        return mapped_column(
            ForeignKey(
                'company.id',
                ondelete='CASCADE',
            ),
            nullable=self._company_id_nullable,
            unique=self._company_id_unique,
        )

    @declared_attr
    def company(self) -> Mapped['CompanyModel']:
        return relationship(
            'CompanyModel',
            back_populates=self._company_back_populates,
        )
