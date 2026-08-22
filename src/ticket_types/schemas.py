from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TicketTypeCreate(BaseModel):
    event_id: UUID
    name: str = Field(min_length=1)
    price: float = Field(ge=0)
    quantity_total: int = Field(gt=0)


class TicketTypeResponse(BaseModel):
    id: UUID
    event_id: UUID
    name: str
    price: float
    quantity_total: int
    quantity_sold: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class TicketTypeResponseList(BaseModel):
    ticket_types: list[TicketTypeResponse]

    model_config = ConfigDict(from_attributes=True)
