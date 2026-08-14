from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Barcha domain Pydantic schemalari (`schemas.py`) shu klassdan meros oladi.

    `from_attributes=True` — SQLAlchemy ORM obyektidan to'g'ridan-to'g'ri
    (masalan `EventRead.model_validate(event_model)`) o'qishga imkon beradi.
    """

    model_config = ConfigDict(from_attributes=True)
