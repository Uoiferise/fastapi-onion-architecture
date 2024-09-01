"""The package contains various data used in tests."""

__all__ = [
    'FakeBaseService',
    'FakeCompanyService',
    'FakeUnitOfWork',
    'FakeUserService',
    'postgres',
    'test_cases',
]

from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.services import CompanyService, UserService
from src.repositories import CompanyRepository, UserRepository
from src.utils.service import BaseService
from src.utils.unit_of_work import UnitOfWork
from tests.fixtures import postgres, test_cases


class FakeUnitOfWork(UnitOfWork):
    """Test class for overriding the standard UnitOfWork.
    Provides isolation using transactions at the level of a single TestCase.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    async def __aenter__(self) -> None:
        self.company = CompanyRepository(self._session)
        self.user = UserRepository(self._session)

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._session.flush()


class FakeBaseService(BaseService):
    """..."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.uow = FakeUnitOfWork(session)


class FakeUserService(FakeBaseService, UserService):
    """..."""

    base_repository: str = 'user'


class FakeCompanyService(FakeBaseService, CompanyService):
    """..."""

    base_repository: str = 'company'
