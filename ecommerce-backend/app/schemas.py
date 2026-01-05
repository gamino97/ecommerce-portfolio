import datetime
import decimal
import uuid
from typing import Annotated

from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict, Field, computed_field


class UserRead(schemas.BaseUser[uuid.UUID]):
    first_name: str
    last_name: str
    created_at: datetime.datetime


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str
    last_name: str


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    id: uuid.UUID


class CategoryCreate(CategoryRead):
    pass


class CategoryUpdate(CategoryRead):
    pass


type ProductPrice = Annotated[
    decimal.Decimal, Field(allow_inf_nan=False, decimal_places=2, gt=0)
]


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    description: str
    image_url: str
    price: ProductPrice
    stock: int
    category_id: uuid.UUID


class ProductReadWithCategory(ProductRead):
    category: CategoryRead


class ProductCreate(BaseModel):
    name: str
    description: str
    image_url: str
    price: ProductPrice
    stock: int = Field(ge=0)
    category_id: uuid.UUID


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    image_url: str | None = None
    price: ProductPrice | None = None
    stock: int | None = Field(ge=0, default=None)
    category_id: uuid.UUID | None = None


class OrderItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: uuid.UUID
    quantity: int
    product: ProductRead
    price: ProductPrice


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    shipping_address: str = Field(min_length=1, max_length=200)
    created_at: datetime.datetime
    order_items: list[OrderItemRead]

    @computed_field
    def total_price(self) -> decimal.Decimal:
        return sum(
            (item.price * item.quantity for item in self.order_items),
            start=decimal.Decimal(0),
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
