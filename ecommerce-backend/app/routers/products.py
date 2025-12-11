import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.db import Category, Product, SessionDep
from app.schemas import ProductCreate, ProductRead, ProductUpdate
from app.services.products import ProductsService
from app.users import current_superuser

router = APIRouter()


@router.get("/products/", response_model=list[ProductRead])
async def read_products(session: SessionDep):
    result = await session.execute(select(Product))
    return result.scalars().all()


@router.get("/products/{product_id}", response_model=ProductRead)
async def read_product(product_id: uuid.UUID, session: SessionDep):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


async def validate_category_exists(session: SessionDep, category_id: uuid.UUID):
    category = await session.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid category_id",
        )


@router.post(
    "/products/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(current_superuser)],
)
async def create_product(product: ProductCreate, session: SessionDep):
    await validate_category_exists(session, product.category_id)
    db_product = Product(**product.model_dump())
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return db_product


@router.patch(
    "/products/{product_id}",
    response_model=ProductRead,
    dependencies=[Depends(current_superuser)],
)
async def update_product(
    product_id: uuid.UUID, product_update: ProductUpdate, session: SessionDep
):
    db_product = await session.get(Product, product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    product_data = product_update.model_dump(exclude_unset=True)
    if "category_id" in product_data:
        await validate_category_exists(session, product_data["category_id"])

    for key, value in product_data.items():
        setattr(db_product, key, value)
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return db_product


@router.get(
    "/products/low-stock/count", dependencies=[Depends(current_superuser)]
)
async def get_low_stock_products_count(session: SessionDep) -> dict[str, int]:
    return await ProductsService.get_low_stock_products_count(session)
