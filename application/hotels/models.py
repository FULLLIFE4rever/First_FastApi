from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    # Убирает предупреждения отсутствия импорта и неприятные подчеркивания в
    # PyCharm и VSCode
    from hotels.rooms.models import Rooms


class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    services: Mapped[Optional[list[str]]] = mapped_column(JSON)
    rooms_quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[str]
    room: Mapped[List["Rooms"]] = relationship(back_populates="hotel")

    def __str__(self):
        return f"Hotel {self.name}"


# class Hotels(Base):
#     __tablename__ = "hotels"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     location = Column(String, nullable=False)
#     services = Column(JSON)
#     rooms_quantity = Column(Integer, nullable=False)
#     image_id = Column(Integer)
#     children = relationship("Rooms", back_populates="rooms")


# class Rooms(Base):
#     __tablename__ = "rooms"

#     id = Column(Integer, primary_key=True)
#     hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
#     name = Column(String, nullable=False)
#     description = Column(String)
#     price = Column(Integer, nullable=False)
#     services = Column(JSON)
#     quantity = Column(Integer)
#     image_id = Column(Integer)
#     hotel = relationship("Hotels", back_populates="hotels")
