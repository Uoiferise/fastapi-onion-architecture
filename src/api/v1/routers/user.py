"""The module contains base routes for working with user."""

from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.api.v1.services.user import UserService
from src.schemas.user import (
    CreateUserRequest,
    CreateUserResponse,
    UpdateUserRequest,
    UserDB,
    UserFilters,
    UserResponse,
    UsersListResponse,
)

router = APIRouter(prefix='/user')


@router.post(
    path='/',
    status_code=HTTP_201_CREATED,
)
async def create_user(
    user: CreateUserRequest,
    service: UserService = Depends(UserService),
) -> CreateUserResponse:
    """Create user."""
    created_user: UserDB = await service.create_user(user)
    return CreateUserResponse(payload=created_user)


@router.get(
    path='/{user_id}',
    status_code=HTTP_200_OK,
)
async def get_user(
    user_id: UUID4,
    service: UserService = Depends(),
) -> UserResponse:
    """Get user by ID."""
    user: UserDB | None = await service.get_user_by_id(user_id)
    return UserResponse(payload=user)


@router.put(
    path='/{user_id}',
    status_code=HTTP_200_OK,
)
async def update_user(
    user_id: UUID4,
    user: UpdateUserRequest,
    service: UserService = Depends(),
) -> UserResponse:
    """Update user."""
    updated_user: UserDB = await service.update_user(user_id, user)
    return UserResponse(payload=updated_user)


@router.delete(
    path='/{user_id}',
    status_code=HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: UUID4,
    service: UserService = Depends(),
) -> None:
    """Delete user."""
    await service.delete_user(user_id)


@router.get(
    path='/filters/',
    status_code=HTTP_200_OK,
)
async def get_users_by_filters(
    filters: UserFilters = Depends(),
    service: UserService = Depends(),
) -> UsersListResponse:
    """Get users by filters."""
    users = await service.get_users_by_filters(filters)
    return UsersListResponse(payload=users)
