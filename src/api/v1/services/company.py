from typing import TYPE_CHECKING

from pydantic import UUID4

from src.schemas.company import CompanyDB, CompanyWithUsers, CreateCompanyRequest
from src.utils.constans import COMPANY_NOT_FOUND_MSG
from src.utils.service import BaseService, transaction_mode

if TYPE_CHECKING:
    from src.models import CompanyModel


class CompanyService(BaseService):
    _repo: str = 'company'

    @transaction_mode
    async def create_company(self, company: CreateCompanyRequest) -> CompanyDB:
        """Create company."""
        created_company: CompanyModel = await self.uow.company.add_one_and_get_obj(**company.model_dump())
        return created_company.to_schema()

    @transaction_mode
    async def get_company_with_users(self, company_id: UUID4) -> CompanyWithUsers:
        """Find company by ID with all users."""
        company: CompanyModel | None = await self.uow.company.get_company_with_users(company_id)
        self.check_existence(obj=company, details=COMPANY_NOT_FOUND_MSG)
        return CompanyWithUsers(
            id=company.id,
            inn=company.inn,
            company_name=company.company_name,
            is_active=company.is_active,
            users=[user.to_schema() for user in company.users],
        )
