from collections.abc import Sequence
from typing import Any
from uuid import UUID

from src.utils.unit_of_work import UnitOfWork


class BaseService:
    """A basic service for performing standard CRUD operations with the base repository.

    params:
        - base_repository: should be string like AbstractUnitOfWork class params
    """

    base_repository: str = None

    @classmethod
    async def add_one(
            cls,
            uow: UnitOfWork,
            **kwargs: Any,
    ) -> None:
        async with uow:
            await uow.__dict__[cls.base_repository].add_one(**kwargs)

    @classmethod
    async def add_one_and_get_id(
            cls,
            uow: UnitOfWork,
            **kwargs: Any,
    ) -> int | str:
        async with uow:
            return await uow.__dict__[cls.base_repository].add_one_and_get_id(**kwargs)

    @classmethod
    async def add_one_and_get_obj(
            cls,
            uow: UnitOfWork,
            **kwargs: Any,
    ) -> Any:
        async with uow:
            return await uow.__dict__[cls.base_repository].add_one_and_get_obj(**kwargs)

    @classmethod
    async def get_by_query_one_or_none(
            cls,
            uow: UnitOfWork,
            **kwargs: Any,
    ) -> Any | None:
        async with uow:
            return await uow.__dict__[cls.base_repository].get_by_query_one_or_none(**kwargs)

    @classmethod
    async def get_by_query_all(
            cls,
            uow: UnitOfWork,
            **kwargs: Any,
    ) -> Sequence[Any]:
        async with uow:
            return await uow.__dict__[cls.base_repository].get_by_query_all(**kwargs)

    @classmethod
    async def update_one_by_id(
            cls,
            uow: UnitOfWork,
            _id: int | str | UUID,
            values: dict,
    ) -> Any:
        async with uow:
            return await uow.__dict__[cls.base_repository].update_one_by_id(_id=_id, values=values)

    @classmethod
    async def delete_by_query(
            cls,
            uow: UnitOfWork,
            **kwargs: Any,
    ) -> None:
        async with uow:
            await uow.__dict__[cls.base_repository].delete_by_query(**kwargs)

    @classmethod
    async def delete_all(
            cls,
            uow: UnitOfWork,
    ) -> None:
        async with uow:
            await uow.__dict__[cls.base_repository].delete_all()
