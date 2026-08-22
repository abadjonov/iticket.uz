from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base, UUIDMixin

if TYPE_CHECKING:
    from src.events.models import Event


class Venue(Base, UUIDMixin):
    __tablename__ = "venues"

    name: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    capacity: Mapped[int] = mapped_column(nullable=False)

    events: Mapped[List["Event"]] = relationship(back_populates="venue")
