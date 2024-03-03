from sqlalchemy import select, update

from base.services import BaseService
from database import async_session
from hotels.models import Hotels


class HotelsService(BaseService):
    model = Hotels

    @classmethod
    async def find_all(cls, location: str | None = None):
        query = select(cls.model.__table__.columns)
        if location:
            search = f"%{location}%"
            query = query.filter(Hotels.location.like(search))
        async with async_session() as session:
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def update_image(cls, image_str: str, hotel_id: int) -> None:
        query = (
            update(Hotels)
            .values(image_id=image_str)
            .filter(Hotels.id == hotel_id)
        )
        async with async_session() as session:
            await session.execute(query)
            await session.commit()
