from sqlalchemy import select

from src.core.database import AsyncSession
from src.categories.models import category


class CategoryRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_category_by_name(self, name: str) -> category | None:
        stmt = select(category).where(category.name == name)
        result = await self.db.execute(stmt)
        category = result.scalar_one_or_none()
        return category

    async def create_category(self, category: category) -> category:
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def get_categories(self) -> list[category]:
        stmt = select(category)
        result = await self.db.execute(stmt)
        return result.scalars()  # type: ignore
