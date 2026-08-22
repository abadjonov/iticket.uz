from sqlalchemy import select

from src.core.database import AsyncSession
from src.ticket_types.models import TicketType


class TicketTypeRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_ticket_type_by_name(self, event_id: str, name: str) -> TicketType | None:
        stmt = select(TicketType).where(TicketType.event_id == event_id, TicketType.name == name)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_ticket_type(self, ticket_type: TicketType) -> TicketType:
        self.db.add(ticket_type)
        await self.db.commit()
        await self.db.refresh(ticket_type)
        return ticket_type

    async def get_ticket_types(self, event_id: str | None = None) -> list[TicketType]:
        stmt = select(TicketType)
        if event_id is not None:
            stmt = stmt.where(TicketType.event_id == event_id)
        result = await self.db.execute(stmt)
        return list(result.scalars())
