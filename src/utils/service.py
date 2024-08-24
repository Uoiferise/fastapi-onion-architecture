"""The module contains base service."""

from collections.abc import Sequence
from typing import Any
from uuid import UUID

from src.utils.unit_of_work import UnitOfWork, transaction_mode


class BaseService:
    """A basic service for performing standard CRUD operations with the base repository.

    params:
        - base_repository: should be string like AbstractUnitOfWork class params
    """

    base_repository: str

    def __init__(self) -> None:
        self.uow: UnitOfWork = UnitOfWork()

    @transaction_mode
    async def add_one(self, **kwargs: Any) -> None:
        await self.uow.__dict__[self.base_repository].add_one(**kwargs)

    @transaction_mode
    async def add_one_and_get_id(self, **kwargs: Any) -> int | str:
        return await self.uow.__dict__[self.base_repository].add_one_and_get_id(**kwargs)

    @transaction_mode
    async def add_one_and_get_obj(self, **kwargs: Any) -> Any:
        return await self.uow.__dict__[self.base_repository].add_one_and_get_obj(**kwargs)

    @transaction_mode
    async def get_by_query_one_or_none(self, **kwargs: Any) -> Any | None:
        return await self.uow.__dict__[self.base_repository].get_by_query_one_or_none(**kwargs)

    @transaction_mode
    async def get_by_query_all(self, **kwargs: Any) -> Sequence[Any]:
        return await self.uow.__dict__[self.base_repository].get_by_query_all(**kwargs)

    @transaction_mode
    async def update_one_by_id(self, obj_id: int | str | UUID, **kwargs: Any) -> Any:
        return await self.uow.__dict__[self.base_repository].update_one_by_id(obj_id, **kwargs)

    @transaction_mode
    async def delete_by_query(self, **kwargs: Any) -> None:
        await self.uow.__dict__[self.base_repository].delete_by_query(**kwargs)

    @transaction_mode
    async def delete_all(self) -> None:
        await self.uow.__dict__[self.base_repository].delete_all()
