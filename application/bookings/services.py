from datetime import date, datetime, timezone

from sqlalchemy import select

from base.services import BaseService
from bookings.models import Bookings
from database import async_session
from hotels.rooms.models import Rooms
from utils.exceptions import ConflictException


class BookingsService(BaseService):
    model = Bookings

    @classmethod
    async def find_by_all(
        cls, user_id: int, before: bool = False
    ) -> list[Bookings]:
        query = (
            select(Bookings.__table__.columns)
            .join(Rooms, Rooms.id == Bookings.room_id)
            .where(Bookings.user_id == user_id)
        )
        if before:
            query = query.where(Bookings.date_to < datetime.now(timezone.utc))
        else:
            query = query.where(Bookings.date_to > datetime.now(timezone.utc))
        print(query)
        async with async_session() as session:
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def find_one(
        cls, price: int, date_from: date, date_to: date, hotel_id: int
    ) -> Rooms:
        boocked_rooms = (
            select(Rooms)
            .join(Bookings, Rooms.id == Bookings.room_id)
            .where(
                (Rooms.price == price)
                & (Rooms.hotel_id == hotel_id)
                & (
                    (Bookings.date_to > date_from)
                    & (Bookings.date_from < date_to)
                )
            )
        ).subquery()
        query = (
            select(Rooms)
            .outerjoin_from(
                Rooms, boocked_rooms, Rooms.id == boocked_rooms.c.id
            )
            .where(
                (Rooms.price == price)
                & (Rooms.hotel_id == hotel_id)
                & (boocked_rooms.c.id == None)  # noqa
            )
        )
        async with async_session() as session:
            result = await session.execute(query)
            return result.scalars().first()

    @classmethod
    async def add(
        cls,
        price: int,
        date_from: date,
        date_to: date,
        user_id: int,
        hotel_id: int,
    ):
        result: Rooms = await cls.find_one(
            price=price,
            date_from=date_from,
            date_to=date_to,
            hotel_id=hotel_id,
        )
        if result is None:
            raise ConflictException("No more avalible rooms")

        result: Bookings = await super().add(
            price=price,
            user_id=user_id,
            room_id=result.id,
            date_from=date_from,
            date_to=date_to,
        )
        return result.mappings().one()
