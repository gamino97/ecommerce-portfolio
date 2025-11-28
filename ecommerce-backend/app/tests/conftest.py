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
