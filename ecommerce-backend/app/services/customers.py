from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import User


class CustomerService:
    @staticmethod
    async def get_customers_count(session: AsyncSession):
        query = select(func.count()).select_from(User)
        result = await session.execute(query)
        return {"count": result.scalar()}

    @staticmethod
    async def get_customers(session: AsyncSession) -> Sequence[User]:
        result = await session.execute(select(User))
        return result.scalars().all()
