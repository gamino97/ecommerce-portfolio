from fastapi import APIRouter, Depends

from app.db import SessionDep
from app.schemas import UserRead
from app.services.customers import CustomerService
from app.users import current_superuser

router = APIRouter()


@router.get(
    "/customers/",
    response_model=list[UserRead],
    dependencies=[Depends(current_superuser)],
)
async def read_customers(session: SessionDep):
    return await CustomerService.get_customers(session)


@router.get(
    "/customers/count",
    dependencies=[Depends(current_superuser)],
)
async def count_customers(session: SessionDep):
    return await CustomerService.get_customers_count(session)
