import datetime
import decimal
import uuid
from typing import Annotated

from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict, Field, computed_field
from pydantic.types import condecimal


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
    price: condecimal(gt=0)
    stock: int
    category_id: uuid.UUID


class ProductCreate(BaseModel):
    name: str
    description: str
    image_url: str
    price: condecimal(gt=0)
    stock: int
    category_id: uuid.UUID


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    image_url: str | None = None
    price: condecimal(gt=0) | None = None
    stock: int | None = None
    category_id: uuid.UUID | None = None


class OrderItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: uuid.UUID
    quantity: int
    product: ProductRead


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    shipping_address: str = Field(min_length=1, max_length=200)
    created_at: datetime.datetime
    user_id: uuid.UUID
    order_items: list[OrderItemRead]

    @computed_field
    def total_price(self) -> decimal.Decimal:
        return sum(
            item.product.price * item.quantity for item in self.order_items
        )


class OrderReadWithUser(OrderRead):
    user: UserRead


class OrderItemCreate(BaseModel):
    product_id: uuid.UUID
    quantity: int


class OrderCreate(BaseModel):
    shipping_address: str = Field(min_length=1, max_length=200)


type CartItem = dict[uuid.UUID, Annotated[int, Field(ge=0)]]


class CartRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: uuid.UUID | None
    items: CartItem


class CartCreate(BaseModel):
    user_id: uuid.UUID | None = None
    items: CartItem


class CartUpdate(BaseModel):
    user_id: uuid.UUID | None = None
    items: CartItem
