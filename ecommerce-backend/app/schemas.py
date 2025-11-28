import uuid

from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict


class UserRead(schemas.BaseUser[uuid.UUID]):
    first_name: str
    last_name: str


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str
    last_name: str


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str


class CategoryCreate(CategoryRead):
    pass


class CategoryUpdate(CategoryRead):
    pass


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    description: str
    image_url: str
    price: float
    stock: int
    category_id: uuid.UUID


class ProductCreate(BaseModel):
    name: str
    description: str
    image_url: str
    price: float
    stock: int
    category_id: uuid.UUID


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    image_url: str | None = None
    price: float | None = None
    stock: int | None = None
    category_id: uuid.UUID | None = None
