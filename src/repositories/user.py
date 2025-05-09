from collections.abc import Sequence

from sqlalchemy import Result, select

from src.models import UserModel
from src.schemas.user import UserFilters
from src.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository[UserModel]):
    _model = UserModel

    async def get_users_by_filter(self, filters: UserFilters) -> Sequence[UserModel]:
        """Find all users by filters."""
        query = select(self._model)

        if filters.ids:
            query = query.where(self._model.id.in_(filters.ids))

        if filters.first_name:
            query = query.where(self._model.first_name.in_(filters.first_name))

        if filters.last_name:
            query = query.where(self._model.last_name.in_(filters.last_name))

        if filters.middle_name:
            query = query.where(self._model.middle_name.in_(filters.middle_name))

        res: Result = await self._session.execute(query)
        return res.scalars().all()
