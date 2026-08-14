from fastapi import APIRouter, Depends

from src.core.database import get_db, AsyncSession
from src.auth.schemas import UserRegisterRequest
from src.users.schemas import UserBase
from src.users.service import UserService
from src.users.repository import UserRepository


router = APIRouter()


@router.post("/register", response_model=UserBase)
async def register_user(user: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    created_user = await user_service.create_user(user)
    return created_user
