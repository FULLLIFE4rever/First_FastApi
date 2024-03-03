from typing import List

from fastapi import APIRouter, Depends, UploadFile
from fastapi_cache.decorator import cache
from utils.utils import add_image
from users.dependencies import get_permission_user

from hotels.rooms.routers import rooms_router
from hotels.schemas import SHotelsCreate, SHotelsInfo
from hotels.services import HotelsService

hotels_router = APIRouter(prefix="/hotels", tags=["Hotels"])
hotels_router.include_router(rooms_router)


@hotels_router.get("/{hotel_id}")
@cache(expire=300)
async def get_hotels_by_id(hotel_id: int) -> List[SHotelsInfo]:
    return await HotelsService.find_one_or_none(id=hotel_id)


@hotels_router.get("")
@cache(expire=3600)
async def get_hotels(location: str | None = None) -> List[SHotelsInfo]:
    return await HotelsService.find_all(location=location)


@hotels_router.post("", dependencies=[Depends(get_permission_user)])
async def create_hotels(hotel: SHotelsCreate = Depends()):
    image_id = add_image("/hotels", hotel.image_id)
    model = await HotelsService.add(
        name=hotel.name,
        location=hotel.location,
        services=hotel.services,
        image_id=image_id,
    )
    return model
