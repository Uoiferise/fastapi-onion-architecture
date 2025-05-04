"""The module contains base classes for working with databases."""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Generic, Never, TypeVar
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import BaseModel

if TYPE_CHECKING:
    from sqlalchemy.engine import Result


class AbstractRepository(ABC):
    """An abstract class implementing the CRUD operations for working with any database."""

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


M = TypeVar('M', bound=BaseModel)


class SqlAlchemyRepository(AbstractRepository, Generic[M]):
    """Basic repository implementing basic CRUD functions with a basic table.
    The repository works using the SqlAlchemy library.
    """

    _model: type[M]  # must be a child class of SQLAlchemy DeclarativeBase

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_one(self, **kwargs: Any) -> None:
        query = insert(self._model).values(**kwargs)
        await self._session.execute(query)

    async def add_one_and_get_id(self, **kwargs: Any) -> int | str | UUID:
        query = insert(self._model).values(**kwargs).returning(self._model.id)
        obj_id: Result = await self._session.execute(query)
        return obj_id.scalar_one()

    async def add_one_and_get_obj(self, **kwargs: Any) -> M:
        query = insert(self._model).values(**kwargs).returning(self._model)
        obj: Result = await self._session.execute(query)
        return obj.scalar_one()

    async def bulk_add(self, values: Sequence[dict[str, Any]]) -> None:
        query = insert(self._model).values(values)
        await self._session.execute(query)

    async def get_by_filter_one_or_none(self, **kwargs: Any) -> M | None:
        query = select(self._model).filter_by(**kwargs)
        res: Result = await self._session.execute(query)
        return res.unique().scalar_one_or_none()

    async def get_by_filter_all(self, **kwargs: Any) -> Sequence[M]:
        query = select(self._model).filter_by(**kwargs)
        res: Result = await self._session.execute(query)
        return res.scalars().all()

    async def update_one_by_id(self, obj_id: int | str | UUID, **kwargs: Any) -> M | None:
        query = update(self._model).filter(self._model.id == obj_id).values(**kwargs).returning(self._model)
        obj: Result | None = await self._session.execute(query)
        return obj.scalar_one_or_none()

    async def delete_by_filter(self, **kwargs: Any) -> None:
        query = delete(self._model).filter_by(**kwargs)
        await self._session.execute(query)

    async def delete_by_ids(self, *args: int | str | UUID) -> None:
        query = delete(self._model).filter(self._model.id.in_(args))
        await self._session.execute(query)

    async def delete_all(self) -> None:
        query = delete(self._model)
        await self._session.execute(query)
