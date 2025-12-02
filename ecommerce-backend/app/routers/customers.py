from fastapi import APIRouter
from sqlalchemy import select

from app.db import SessionDep, User
from app.schemas import UserRead

router = APIRouter()


@router.get("/customers/", tags=["customers"], response_model=list[UserRead])
async def read_customers(session: SessionDep):
    result = await session.execute(select(User))
    return result.scalars().all()
