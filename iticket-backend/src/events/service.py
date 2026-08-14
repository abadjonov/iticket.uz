from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from . import repository, models


async def create_event(db: AsyncSession, data: Dict[str, Any], organizer_id: int | None = None) -> models.Event:
	event = models.Event(**{**data, "organizer_id": organizer_id})
	return await repository.create_event(db, event)


async def update_event(db: AsyncSession, event: models.Event, values: Dict[str, Any]) -> models.Event:
	return await repository.update_event(db, event, values)


async def publish_event(db: AsyncSession, event: models.Event) -> models.Event:
	return await repository.update_event(db, event, {"published": True})
