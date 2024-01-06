__all__ = [
    'router'
]

import asyncio

from loguru import logger
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.database.db import get_async_session
from src.metadata import ERRORS_MAP
from src.api.v1.routers import v1_user_router

router = APIRouter()
router.include_router(v1_user_router, prefix='/v1', tags=['v1'])


@router.get('/healthz/', tags=['healthz'])
async def health_check(session: AsyncSession = Depends(get_async_session)):
    async def check_service(service: str):
        try:
            if service == 'postgres':
                await session.execute(text('SELECT 1'))
        except Exception as exc:
            logger.error(f'Health check failed with error: {exc}')
            raise HTTPException(status_code=400, detail=ERRORS_MAP.get(service))

    await asyncio.gather(*[
        check_service('postgres'),
    ])

    return JSONResponse(
        status_code=200,
        content={}
    )
