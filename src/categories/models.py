from typing import List
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base, UUIDMixin

if TYPE_CHECKING:
    from src.events.models import Event


class Category(Base, UUIDMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(nullable=False)
    slug: Mapped[str] = mapped_column(unique=True, nullable=False)

    events: Mapped[List["Event"]] = relationship(back_populates="category")
