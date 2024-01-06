from typing import Optional, Union, Any, Sequence
from uuid import uuid4

from src.utils.unit_of_work import UnitOfWork


class BaseService:
    """
    A basic service for performing standard CRUD operations with the base repository.

    params:
        - base_repository: should be string like AbstractUnitOfWork class params
    """

    base_repository: str = None

    @classmethod
    async def add_one(
            cls,
            uow: UnitOfWork,
            **kwargs
    ) -> None:
        async with uow:
            await uow.__dict__[cls.base_repository].add_one(**kwargs)

    @classmethod
    async def add_one_and_get_id(
            cls,
            uow: UnitOfWork,
            **kwargs
    ) -> Union[int, str]:
        async with uow:
            _id = await uow.__dict__[cls.base_repository].add_one_and_get_id(**kwargs)
            return _id

    @classmethod
    async def add_one_and_get_obj(
            cls,
            uow: UnitOfWork,
            **kwargs
    ) -> Any:
        async with uow:
            _obj = await uow.__dict__[cls.base_repository].add_one_and_get_obj(**kwargs)
            return _obj

    @classmethod
    async def get_by_query_one_or_none(
            cls,
            uow: UnitOfWork,
            **kwargs
    ) -> Optional[Any]:
        async with uow:
            _result = await uow.__dict__[cls.base_repository].get_by_query_one_or_none(**kwargs)
            return _result

    @classmethod
    async def get_by_query_all(
            cls,
            uow: UnitOfWork,
            **kwargs
    ) -> Sequence[Any]:
        async with uow:
            _result = await uow.__dict__[cls.base_repository].get_by_query_all(**kwargs)
            return _result

    @classmethod
    async def update_one_by_id(
            cls,
            uow: UnitOfWork,
            _id: Union[int, str, uuid4],
            values: dict
    ) -> Any:
        async with uow:
            _obj = await uow.__dict__[cls.base_repository].update_one_by_id(_id=_id, values=values)
            return _obj

    @classmethod
    async def delete_by_query(
            cls,
            uow: UnitOfWork,
            **kwargs
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
