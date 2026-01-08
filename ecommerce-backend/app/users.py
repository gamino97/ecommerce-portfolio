import contextlib
import logging
import uuid

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.exceptions import UserAlreadyExists
from sqlalchemy import select

from app.db import User, get_async_session, get_user_db
from app.schemas import UserCreate

from .config import get_settings

settings = get_settings()
SECRET = settings.secret
logger = logging.getLogger("app")


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(
        self, user: User, request: Request | None = None
    ):
        logger.info(f"User {user.id} has registered.")


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy[models.UP, models.ID]:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(superuser=True, active=True)


async def create_user(
    email: str,
    password: str,
    is_superuser: bool = False,
    first_name: str = "",
    last_name: str = "",
):
    get_async_session_context = contextlib.asynccontextmanager(
        get_async_session
    )
    get_user_db_context = contextlib.asynccontextmanager(get_user_db)
    get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    result = await session.execute(
                        select(User).where(User.email == email)
                    )
                    user = result.scalar_one_or_none()
                    if user is not None:
                        return user
                    user = await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                            first_name=first_name,
                            last_name=last_name,
                        )
                    )
                    logger.info("User created %s", user)
                    return user
    except UserAlreadyExists:
        logger.info("User %s already exists", email)
        raise
