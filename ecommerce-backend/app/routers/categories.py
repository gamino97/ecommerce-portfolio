from fastapi import APIRouter
from sqlalchemy import select

from app.db import Category, SessionDep
from app.schemas import CategoryRead

router = APIRouter()


@router.get("/categories/", response_model=list[CategoryRead])
async def read_categories(session: SessionDep):
    result = await session.execute(select(Category))
    return result.scalars().all()
