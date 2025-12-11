from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Product


class ProductsService:

    @staticmethod
    async def get_low_stock_products_count(
        session: AsyncSession,
    ) -> dict[str, int]:
        query = (
            select(func.count()).select_from(Product).where(Product.stock < 30)
        )
        result = await session.execute(query)
        return {"count": result.scalar() or 0}
