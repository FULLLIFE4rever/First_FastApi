from typing import Optional

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bookings.models import Bookings
from database import Base
from hotels.models import Hotels


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(
        ForeignKey("hotels.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    services: Mapped[Optional[list[str]]] = mapped_column(JSON, nullable=False)
    image_id: Mapped[int]
    hotel: Mapped["Hotels"] = relationship(back_populates="room")
    bookings: Mapped["Bookings"] = relationship(back_populates="room")

    def __str__(self):
        return f"Room {self.name}"
