from fastapi import APIRouter, Depends

from src.core.database import get_db, AsyncSession
from src.auth.dependencies import get_current_active_user, get_current_orginizer
from src.organizers.models import Organizer
from src.ticket_types.models import TicketType
from src.ticket_types.repository import TicketTypeRepository
from src.ticket_types.schemas import TicketTypeCreate, TicketTypeResponse, TicketTypeResponseList
from src.ticket_types.service import TicketTypeService


router = APIRouter()


@router.post("/", response_model=TicketTypeResponse)
async def create_category(
    data: TicketTypeCreate,
    organizer: Organizer = Depends(get_current_orginizer),
    db: AsyncSession = Depends(get_db),
) -> TicketType:
    service = TicketTypeService(TicketTypeRepository(db))
    return await service.create_ticket_type(data)


@router.get("/", response_model=TicketTypeResponseList)
async def get_ticket_type_list(
    event_id: str | None = None,
    user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> TicketTypeResponseList:
    service = TicketTypeService(TicketTypeRepository(db))
    ticket_types = await service.get_ticket_types(event_id)
    return TicketTypeResponseList(ticket_types=ticket_types)  # type: ignore
