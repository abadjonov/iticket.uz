from fastapi import HTTPException, status

from src.users.models import User
from src.users.schemas import UserBase
from src.users.repository import UserRepository
from src.auth.schemas import UserRegisterRequest
from src.core.security import hash_password, verify_password


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def get_user_by_id(self, user_id: str) -> User | None:
        return await self.user_repository.get_user_by_id(user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.user_repository.get_user_by_email(email)

    async def create_user(self, user: UserRegisterRequest) -> User:
        existing_user = await self.user_repository.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email allaqachon ro'yxatdan o'tgan",
            )

        hashed_password = hash_password(user.password)
        new_user = User(email=user.email, hashed_password=hashed_password)
        return await self.user_repository.create_user(new_user)

    async def update_user(self, user: User) -> User:
        return await self.user_repository.update_user(user)

    async def delete_user(self, user: User) -> None:
        await self.user_repository.delete_user(user)
