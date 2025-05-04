from fastapi import HTTPException
from pydantic import UUID4
from starlette.status import HTTP_404_NOT_FOUND

from src.models import CompanyModel
from src.schemas.company import CompanyWithUsers, CreateCompanyRequest
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class CompanyService(BaseService):
    base_repository: str = 'company'

    @transaction_mode
    async def create_company(self, company: CreateCompanyRequest) -> CompanyModel:
        """Create company."""
        return await self.uow.company.add_one_and_get_obj(**company.model_dump())

    @transaction_mode
    async def get_company_with_users(self, company_id: UUID4) -> CompanyWithUsers:
        """Find company by ID with all users."""
        company: CompanyModel | None = await self.uow.company.get_company_with_users(company_id)
        self._check_company_exists(company)
        return CompanyWithUsers(
            id=company.id,
            inn=company.inn,
            company_name=company.company_name,
            is_active=company.is_active,
            users=[user.to_schema() for user in company.users],
        )

    @staticmethod
    def _check_company_exists(company: CompanyModel | None) -> None:
        if not company:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='User not found')
