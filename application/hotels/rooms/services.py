from base.services import BaseService
from hotels.rooms.models import Rooms


class RoomsService(BaseService):
    model = Rooms
