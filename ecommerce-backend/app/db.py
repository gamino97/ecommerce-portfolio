from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql.json import JSON
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .config import get_settings

settings = get_settings()
DATABASE_URL = settings.database_url


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))
    orders: Mapped[list["Order"]] = relationship(back_populates="user")
    carts: Mapped[list["Cart"]] = relationship(back_populates="user")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=func.gen_random_uuid()
    )
    name: Mapped[str] = mapped_column(String(150), unique=True)
    products: Mapped[list["Product"]] = relationship(back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=func.gen_random_uuid()
    )
    name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(String(1000))
    image_url: Mapped[str] = mapped_column(String(500))
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    stock: Mapped[int] = mapped_column(default=0)
    category_id: Mapped[UUID] = mapped_column(ForeignKey("categories.id"))
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    category: Mapped[Category] = relationship(back_populates="products")
    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="product"
    )


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(
        String, CheckConstraint("status IN ('pending', 'shipped', 'canceled')")
    )
    shipping_address: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(back_populates="orders")
    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column()
    order: Mapped[Order] = relationship(back_populates="order_items")
    product: Mapped[Product] = relationship(back_populates="order_items")


class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("user.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    items: Mapped[dict[str, Any]] = mapped_column(JSON(), default=dict)
    user: Mapped[User | None] = relationship("User", back_populates="carts")
    is_active: Mapped[bool] = mapped_column(default=True)


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

app_target_metadata = [Base.metadata]
