import json
import logging
import logging.config
from pathlib import Path

from fastapi import FastAPI

from app.routers import carts, categories, customers, orders, products
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, fastapi_users

tags_metadata = [
    {
        "name": "auth",
        "description": "Authentication operations (login, logout, register, etc.)",
    },
    {
        "name": "users",
        "description": "Operations to manage users.",
    },
    {
        "name": "categories",
        "description": "Manage product categories.",
    },
    {
        "name": "products",
        "description": "Manage products (create, read, update, delete).",
    },
    {
        "name": "customers",
        "description": "Manage customer information.",
    },
    {
        "name": "orders",
        "description": "Manage orders (create, list, process).",
    },
    {
        "name": "carts",
        "description": "Manage shopping carts and cart items.",
    },
]

app = FastAPI(
    title="Ecommerce Portfolio API",
    description="API for the Ecommerce Portfolio application.",
    version="1.0.0",
    openapi_tags=tags_metadata,
)


config_file = Path("logging_config.json")
with open(config_file) as f_in:
    config = json.load(f_in)
logging.config.dictConfig(config)
logger = logging.getLogger("app")
logger.info("Application startup complete.")


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    categories.router,
    tags=["categories"],
)
app.include_router(
    products.router,
    tags=["products"],
)
app.include_router(
    customers.router,
    tags=["customers"],
)
app.include_router(
    orders.router,
    tags=["orders"],
)
app.include_router(
    carts.router,
    tags=["carts"],
)
