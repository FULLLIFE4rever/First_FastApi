from typing import List, Literal

from sqlalchemy.orm import Mapped, mapped_column, relationship

from bookings.models import Bookings
from database import Base

Authority = Literal["user", "moderator", "admin"]


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    authority: Mapped[Authority] = mapped_column(server_default="user")
    bookings: Mapped[List["Bookings"]] = relationship(back_populates="user")

    def __str__(self):
        return f"User {self.email}"
