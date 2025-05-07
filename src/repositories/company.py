from pydantic import UUID4
from sqlalchemy import Result, select
from sqlalchemy.orm import selectinload

from src.models import CompanyModel
from src.utils.repository import SqlAlchemyRepository


class CompanyRepository(SqlAlchemyRepository[CompanyModel]):
    _model = CompanyModel

    async def get_company_with_users(self, company_id: UUID4) -> CompanyModel | None:
        """Find company by ID with all users."""
        query = (
            select(self._model)
            .where(self._model.id == company_id)
            .options(selectinload(self._model.users))
        )
        res: Result = await self._session.execute(query)
        return res.scalar_one_or_none()
