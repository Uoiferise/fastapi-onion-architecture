__all__ = [
    'v1_company_router',
    'v1_user_router',
]

from src.api.v1.routers.company import router as v1_company_router
from src.api.v1.routers.user import router as v1_user_router
