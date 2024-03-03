from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings

DATABASE_PARAMS = {}
if settings.TEST_MODE:
    DATABASE_PARAMS["poolclass"] = NullPool
engine = create_async_engine(settings.get_url, **DATABASE_PARAMS)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Alembic/Alcheemy Base class"""

    pass
