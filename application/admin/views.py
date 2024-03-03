from sqladmin import ModelView

from bookings.models import Bookings
from hotels.models import Hotels
from hotels.rooms.models import Rooms
from users.models import Users


class UserAdmin(ModelView, model=Users):
    column_exclude_list = (Users.hashed_password,)
    column_details_exclude_list = (Users.hashed_password,)
    can_create = False
    can_edit = False
    can_delete = False
    name_plural = "Users"
    name = "User"
    icon = "fa-solid fa-user"


class BookingAdmin(ModelView, model=Bookings):
    column_list = "__all__"
    name_plural = "Bookings"
    name = "Booking"
    can_edit = False
    icon = "fa-solid fa-book"


class HotelAdmin(ModelView, model=Hotels):
    column_list = "__all__"
    name_plural = "Hotels"
    name = "Hotel"
    icon = "fa-solid fa-hotel"


class RoomAdmin(ModelView, model=Rooms):
    column_list = "__all__"
    name_plural = "Rooms"
    name = "Room"
    icon = "fa-solid fa-bed"
