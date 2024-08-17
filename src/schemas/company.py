from pydantic import UUID4, BaseModel, Field

from src.schemas.response import BaseCreateResponse, BaseResponse
from src.schemas.user import UserDB


class CompanyID(BaseModel):
    id: UUID4


class CreateCompanyRequest(BaseModel):
    inn: int
    company_name: str = Field(max_length=50)


class UpdateCompanyRequest(CreateCompanyRequest):
    pass


class CompanyDB(CompanyID, CreateCompanyRequest):
    is_active: bool


class CompanyWithUsers(CompanyDB):
    users: list[UserDB] = Field(default_factory=list)


class CreateCompanyResponse(BaseCreateResponse):
    payload: CompanyDB


class CompanyResponse(BaseResponse):
    payload: CompanyWithUsers


class CompanyListResponse(BaseResponse):
    payload: list[CompanyDB]
