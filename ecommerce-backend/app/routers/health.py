from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_async_session

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check(session: AsyncSession = Depends(get_async_session)):
    """
    Health check endpoint to verify backend and database connectivity.
    """
    result = await session.execute(text("SELECT 1"))
    if result.scalar() != 1:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is not responding correctly",
        )
    return {"status": "ok", "database": "connected"}
