from fastapi import HTTPException, status

from src.ticket_types.models import TicketType
from src.ticket_types.repository import TicketTypeRepository
from src.ticket_types.schemas import TicketTypeCreate


class TicketTypeService:
    def __init__(self, repository: TicketTypeRepository) -> None:
        self.repository = repository

    async def create_ticket_type(self, data: TicketTypeCreate) -> TicketType:
        existing_ticket_type = await self.repository.get_ticket_type_by_name(
            str(data.event_id), data.name
        )
        if existing_ticket_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bunday ticket turi oldin yaratilgan.",
            )

        return await self.repository.create_ticket_type(
            TicketType(
                event_id=str(data.event_id),
                name=data.name,
                price=data.price,
                quantity_total=data.quantity_total,
            )
        )

    async def get_ticket_types(self, event_id: str | None = None) -> list[TicketType]:
        return await self.repository.get_ticket_types(event_id)
