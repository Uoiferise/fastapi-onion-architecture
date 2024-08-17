__all__ = [
    'router',
]

import asyncio

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from src.api.v1.routers import v1_company_router, v1_user_router
from src.database.db import get_async_session
from src.metadata import ERRORS_MAP
from src.schemas.response import BaseResponse

router = APIRouter()
router.include_router(v1_user_router, prefix='/v1', tags=['User | v1'])
router.include_router(v1_company_router, prefix='/v1', tags=['Company | v1'])


@router.get(
    path='/healthz/',
    tags=['healthz'],
    status_code=HTTP_200_OK,
)
async def health_check(
        session: AsyncSession = Depends(get_async_session),
) -> BaseResponse:
    """Check api external connection."""
    async def check_service(service: str) -> None:
        try:
            if service == 'postgres':
                await session.execute(text('SELECT 1'))
        except Exception as exc:
            logger.error(f'Health check failed with error: {exc}')
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=ERRORS_MAP.get(service))

    await asyncio.gather(*[
        check_service('postgres'),
    ])

    return BaseResponse()
