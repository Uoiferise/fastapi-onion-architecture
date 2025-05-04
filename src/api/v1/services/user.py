from typing import TYPE_CHECKING

from pydantic import UUID4

from src.schemas.user import CreateUserRequest, UpdateUserRequest, UserDB, UserFilters
from src.utils.constans import USER_NOT_FOUND_MSG
from src.utils.service import BaseService, transaction_mode

if TYPE_CHECKING:
    from collections.abc import Sequence

    from src.models import UserModel


class UserService(BaseService):
    _repo: str = 'user'

    @transaction_mode
    async def create_user(self, user: CreateUserRequest) -> UserDB:
        """Create user."""
        created_user: UserModel = await self.uow.user.add_one_and_get_obj(**user.model_dump())
        return created_user.to_schema()

    @transaction_mode
    async def get_user_by_id(self, user_id: UUID4) -> UserDB:
        """Get user by ID."""
        user: UserModel | None = await self.uow.user.get_by_filter_one_or_none(id=user_id)
        self.check_existence(obj=user, details=USER_NOT_FOUND_MSG)
        return user.to_schema()

    @transaction_mode
    async def update_user(self, user_id: UUID4, user: UpdateUserRequest) -> UserDB:
        """Update user by ID."""
        user: UserModel | None = await self.uow.user.update_one_by_id(obj_id=user_id, **user.model_dump())
        self.check_existence(obj=user, details=USER_NOT_FOUND_MSG)
        return user.to_schema()

    @transaction_mode
    async def delete_user(self, user_id: UUID4) -> None:
        """Delete user by ID."""
        await self.uow.user.delete_by_filter(id=user_id)

    @transaction_mode
    async def get_users_by_filters(self, filters: UserFilters) -> list[UserDB]:
        """Get users by filter."""
        users: Sequence[UserModel] = await self.uow.user.get_users_by_filter(filters)
        return [user.to_schema() for user in users]
