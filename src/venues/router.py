from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Body

from src.core.database import get_db, AsyncSession
from src.users.models import User
from src.auth.dependencies import get_current_active_user, get_current_active_superuser

from src.venues.models import Venue
from src.venues.schemas import VenueCreate, VenueResponse
from src.venues.repository import VenueRepository
from src.venues.service import VenueService


router = APIRouter()


@router.post("/", response_model=VenueResponse)
async def create_venue(
    data: VenueCreate,
    user: User = Depends(get_current_active_superuser),
    db: AsyncSession = Depends(get_db),
) -> Venue:
    venue_repository = VenueRepository(db)
    venue_service = VenueService(venue_repository)
    new_venue = await venue_service.create_venue(data)
    return new_venue
