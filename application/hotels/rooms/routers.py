from typing import List

from fastapi import APIRouter

from hotels.rooms.schemas import SRooms
from hotels.rooms.services import RoomsService

rooms_router = APIRouter(prefix="/{hotel_id:int}/rooms", tags=["Rooms"])


@rooms_router.get("")
async def get_rooms(hotel_id: int) -> List[SRooms]:
    return await RoomsService.find_all(hotel_id=hotel_id)
