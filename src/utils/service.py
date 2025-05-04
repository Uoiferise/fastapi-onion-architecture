"""The module contains base service."""
import functools
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable, Sequence
from typing import Any, Never, TypeVar, overload
from uuid import UUID

from fastapi import Depends, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from src.utils.repository import AbstractRepository
from src.utils.unit_of_work import AbstractUnitOfWork, UnitOfWork

T = TypeVar('T', bound=Callable[..., Awaitable[Any]])


@overload
def transaction_mode(_func: T) -> T: ...
@overload
def transaction_mode(*, auto_flush: bool) -> Callable[[T], T]: ...


def transaction_mode(_func: T | None = None, *, auto_flush: bool = False) -> T | Callable[[T], T]:
    """Wraps the function in transaction mode.
    Checks if the UnitOfWork context manager is open.
    If not, then opens the context manager and opens a transaction.
    """

    def decorator(func: T) -> T:
        @functools.wraps(func)
        async def wrapper(self: AbstractService, *args: Any, **kwargs: Any) -> Any:
            if self.uow.is_open:
                res = await func(self, *args, **kwargs)
                if auto_flush:
                    await self.uow.flush()
                return res
            async with self.uow:
                return await func(self, *args, **kwargs)

        return wrapper

    if _func is None:  # Using with parameters: @transaction_mode(auto_flush=True)
        return decorator
    return decorator(_func)  # Using without parameters: @transaction_mode


class AbstractService(ABC):
    """An abstract class that implements CRUD operations at the service level."""

    uow: AbstractUnitOfWork

    @abstractmethod
    async def add_one(self, *args: Any, **kwargs: Any) -> Never:
        """Adding one entry."""
        raise NotImplementedError

    @abstractmethod
    async def add_one_and_get_id(self, *args: Any, **kwargs: Any) -> Never:
        """Adding one entry and getting the ID of this entry."""
        raise NotImplementedError

    @abstractmethod
    async def add_one_and_get_obj(self, *args: Any, **kwargs: Any) -> Never:
        """Adding one entry and getting that entry."""
        raise NotImplementedError

    @abstractmethod
    async def bulk_add(self, *args: Any, **kwargs: Any) -> Never:
        """Bulk adding of entries."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_filter_one_or_none(self, *args: Any, **kwargs: Any) -> Never:
        """Get one entry for the given filter, if it exists."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_filter_all(self, *args: Any, **kwargs: Any) -> Never:
        """Getting all entries according to the specified filter."""
        raise NotImplementedError

    @abstractmethod
    async def update_one_by_id(self, *args: Any, **kwargs: Any) -> Never:
        """Updating a single entry by its ID."""
        raise NotImplementedError

    @abstractmethod
    async def delete_by_filter(self, *args: Any, **kwargs: Any) -> Never:
        """Bulk deletion of entries by filter."""
        raise NotImplementedError

    @abstractmethod
    async def delete_by_ids(self, *args: Any, **kwargs: Any) -> Never:
        """Bulk deletion of entries by passed IDs."""
        raise NotImplementedError

    @abstractmethod
    async def delete_all(self, *args: Any, **kwargs: Any) -> Never:
        """Bulk delete all entries."""
        raise NotImplementedError


class BaseService(AbstractService):
    """A basic service for performing standard CRUD operations with the base repository."""

    _repo: str | None = None  # must be a string as an attribute of the Abstract UnitOfWork class

    def __init__(self, uow: UnitOfWork = Depends()) -> None:
        """Creates an instance of the base service.

        If the child class has dependencies with another service and wants to use its functionality,
        it is necessary to explicitly specify the dependency via `Depends`, for example:
            def __init__(self, uow: UnitOfWork = Depends(), other_service: OtherService = Depends())
        """
        self.uow: UnitOfWork = uow
        if not hasattr(self, '_repo') or self._repo is None:
            err_msg = f"Attribute '_repo' is required for class {self.__class__.__name__}"
            raise AttributeError(err_msg)

    @transaction_mode
    async def add_one(self, **kwargs: Any) -> None:
        await self._get_related_repo().add_one(**kwargs)

    @transaction_mode
    async def add_one_and_get_id(self, **kwargs: Any) -> int | str | UUID:
        return await self._get_related_repo().add_one_and_get_id(**kwargs)

    @transaction_mode
    async def add_one_and_get_obj(self, **kwargs: Any) -> Any:
        return await self._get_related_repo().add_one_and_get_obj(**kwargs)

    @transaction_mode
    async def bulk_add(self, values: Sequence[dict[str, Any]]) -> None:
        await self._get_related_repo().bulk_add(values=values)

    @transaction_mode
    async def get_by_filter_one_or_none(self, **kwargs: Any) -> Any:
        return await self._get_related_repo().get_by_filter_one_or_none(**kwargs)

    @transaction_mode
    async def get_by_filter_all(self, **kwargs: Any) -> Sequence[Any]:
        return await self._get_related_repo().get_by_filter_all(**kwargs)

    @transaction_mode
    async def update_one_by_id(self, obj_id: int | str | UUID, **kwargs: Any) -> Any:
        return await self._get_related_repo().update_one_by_id(obj_id=obj_id, **kwargs)

    @transaction_mode
    async def delete_by_filter(self, **kwargs: Any) -> None:
        await self._get_related_repo().delete_by_filter(**kwargs)

    @transaction_mode
    async def delete_by_ids(self, *args: int | str | UUID) -> None:
        await self._get_related_repo().delete_by_ids(*args)

    @transaction_mode
    async def delete_all(self) -> None:
        await self._get_related_repo().delete_all()

    @staticmethod
    def check_existence(obj: Any, details: str) -> None:
        """Checking the existence of an object."""
        if not obj:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=details)

    def _get_related_repo(self) -> AbstractRepository:
        """Returns the repository associated with the service."""
        return getattr(self.uow, self._repo)
