import contextlib
from collections.abc import AsyncGenerator

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

from app.db import DATABASE_URL, Base, get_async_session  # noqa: E402
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
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def session(prepare_database) -> AsyncGenerator[AsyncSession, None]:
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
async def auth_client(session: AsyncSession, client: AsyncClient):
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
    token = await get_jwt_strategy().write_token(user)
    client.headers["Authorization"] = f"Bearer {token}"
    yield client
