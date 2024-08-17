"""The module contains base routes for working with company."""

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.schemas.company import CompanyResponse, CompanyWithUsers, CreateCompanyRequest, CreateCompanyResponse
from src.services import CompanyService

if TYPE_CHECKING:
    from src.models import CompanyModel

router = APIRouter(prefix='/company')


@router.post(
    path='/',
    status_code=HTTP_201_CREATED,
)
async def create_company(
        company: CreateCompanyRequest,
        service: CompanyService = Depends(CompanyService),
) -> CreateCompanyResponse:
    """Create user."""
    created_user: CompanyModel = await service.create_company(company)
    return CreateCompanyResponse(payload=created_user.to_pydantic_schema())


@router.get(
    path='/{company_id}',
    status_code=HTTP_200_OK,
)
async def get_company_with_users(
        company_id: UUID4,
        service: CompanyService = Depends(CompanyService),
) -> CompanyResponse:
    """Get user by ID."""
    company: CompanyWithUsers = await service.get_company_with_users(company_id)
    return CompanyResponse(payload=company)
