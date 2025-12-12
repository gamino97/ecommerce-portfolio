import contextlib
from collections.abc import AsyncGenerator
from typing import Callable, Coroutine

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

load_dotenv(".env.test", override=True)

from app.db import (  # noqa: E402
    DATABASE_URL,
    Base,
    Cart,
    Category,
    Product,
    User,
    get_async_session,
)
from app.main import app  # noqa: E402
from app.users import (  # noqa: E402
    UserCreate,
    get_jwt_strategy,
    get_user_db,
    get_user_manager,
)

# Create engine with NullPool to avoid connection reuse issues
engine = create_async_engine(DATABASE_URL, echo=False, poolclass=NullPool)
TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_database():
    """Create tables before each test and drop them after."""
    yield
    async with engine.begin() as conn:
        for tbl in reversed(Base.metadata.sorted_tables):
            await conn.execute(tbl.delete())


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database_cleanup():
    """Create tables before each test and drop them after."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional session for tests."""
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Provide an authenticated AsyncClient."""

    async def override_get_async_session():
        yield session

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def super_user(session: AsyncSession) -> User:
    get_user_db_context = contextlib.asynccontextmanager(get_user_db)
    get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)
    async with get_user_db_context(session) as user_db:
        async with get_user_manager_context(user_db) as user_manager:
            user = await user_manager.create(
                UserCreate(
                    email="test.user2@example.com",
                    password="password123",
                    is_superuser=True,
                    first_name="Test",
                    last_name="User",
                )
            )
            print(f"User created {user}")
            return user


@pytest.fixture
async def user(session: AsyncSession) -> User:
    """Create a sample user for tests."""
    user = User(
        email="test@example.com",
        hashed_password="hashedpassword",
        is_active=True,
        is_superuser=False,
        is_verified=True,
        first_name="Test",
        last_name="User",
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def auth_client(super_user: User, client: AsyncClient):
    token = await get_jwt_strategy().write_token(super_user)
    client.headers["Authorization"] = f"Bearer {token}"
    yield client


@pytest.fixture
async def category(
    create_category: Callable[[str], Coroutine[None, None, Category]],
):
    """Create a sample category for tests."""
    return await create_category("Test Category")


@pytest.fixture
def create_category(
    session: AsyncSession,
) -> Callable[[str], Coroutine[None, None, Category]]:
    async def _create_category(name: str) -> Category:
        category = Category(name=name)
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category

    return _create_category


@pytest.fixture
async def product(session: AsyncSession, category: Category):
    """Create a sample product for tests."""
    product = Product(
        name="Test Product",
        description="A test product",
        image_url="http://example.com/image.png",
        price=10.99,
        stock=100,
        category_id=category.id,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@pytest.fixture
def create_product(
    session: AsyncSession,
):
    async def _create_product(
        name: str, category: Category, price: str = "10.99", stock: int = 100
    ) -> Product:
        product = Product(
            name=name,
            description="A test product",
            image_url="http://example.com/image.png",
            price=price,
            stock=stock,
            category_id=category.id,
        )
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product

    return _create_product


@pytest.fixture
async def cart(session: AsyncSession):
    cart = Cart()
    session.add(cart)
    await session.commit()
    return cart
