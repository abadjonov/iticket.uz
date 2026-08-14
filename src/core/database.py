import uuid
from collections.abc import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.core.config import settings

# Alembic autogenerate barqaror constraint nomlarini yaratishi uchun.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

engine = create_async_engine(settings.DATABASE_URL, echo=settings.ENVIRONMENT == "development")

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Barcha domain SQLAlchemy modellari shu klassdan meros oladi."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class UUIDMixin:
    """`uuid` PK pattern — deyarli barcha jadvallar shu mixin'dan foydalanadi.

    Qarang: [[03-database-schema.md]]
    """

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )


class TimestampMixin:
    """`created_at` va `updated_at` timestamp pattern — deyarli barcha jadvallar shu mixin'dan foydalanadi.

    Qarang: [[03-database-schema.md]]
    """

    created_at: Mapped[str] = mapped_column(
        "created_at",
        default="now()",
        server_default="now()",
        nullable=False,
    )
    updated_at: Mapped[str] = mapped_column(
        "updated_at",
        default="now()",
        server_default="now()",
        onupdate="now()",
        nullable=False,
    )


async def get_db() -> AsyncGenerator[AsyncSession]:
    """FastAPI dependency — har bir so'rov uchun alohida DB session beradi."""
    async with AsyncSessionLocal() as session:
        yield session
