from dataclasses import dataclass

from fastapi import Query
from pydantic import UUID4, BaseModel, Field

from src.schemas.filter import TypeFilter
from src.schemas.response import BaseCreateResponse, BaseResponse


class UserID(BaseModel):
    id: UUID4


class CreateUserRequest(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    middle_name: str | None = Field(max_length=50, default=None)


class UpdateUserRequest(CreateUserRequest):
    pass


class UserDB(UserID, CreateUserRequest):
    pass


class CreateUserResponse(BaseCreateResponse):
    payload: UserDB


class UserResponse(BaseResponse):
    payload: UserDB


class UsersListResponse(BaseResponse):
    payload: list[UserDB]


@dataclass
class UserFilters(TypeFilter):
    ids: list[UUID4] | None = Query(None)
    first_name: list[str] | None = Query(None)
    last_name: list[str] | None = Query(None)
    middle_name: list[str] | None = Query(None)
