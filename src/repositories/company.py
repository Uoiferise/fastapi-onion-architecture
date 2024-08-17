from pydantic import UUID4
from sqlalchemy import Result, select
from sqlalchemy.orm import selectinload

from src.models import CompanyModel
from src.utils.repository import SqlAlchemyRepository


class CompanyRepository(SqlAlchemyRepository):
    model = CompanyModel

    async def get_company_with_users(self, company_id: UUID4) -> CompanyModel | None:
        """Find company by ID with all users."""
        query = (
            select(self.model)
            .where(self.model.id == company_id)
            .options(selectinload(self.model.users))
        )
        res: Result = await self.session.execute(query)
        return res.scalar_one_or_none()
