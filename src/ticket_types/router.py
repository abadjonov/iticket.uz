from fastapi import APIRouter, Depends

from src.core.database import get_db, AsyncSession
from src.users.models import User
from src.auth.dependencies import get_current_orginizer, get_current_active_user


router = APIRouter()


@router.post("/", response_model=)
async def create_category(
    data: ,
    user: User = Depends(get_current_orginizer),
    db: AsyncSession = Depends(get_db),
) -> Category:
    pass


@router.get("/", response_model=)
async def get_category_list(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    pass
