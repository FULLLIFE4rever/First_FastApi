import aiofiles
from fastapi import APIRouter, Depends, UploadFile

from hotels.services import HotelsService
from tasks.tasks import process_pic
from utils.exceptions import ConflictException
from utils.utils import add_image, filename_generator
from config import BASE_DIR

image_router = APIRouter(prefix="/images", tags=["Images"])


@image_router.post("/hotels")
async def add_hotel_image(hotel_id: int, file: UploadFile):
    add_image("/hotels", file)
    await HotelsService.update_image(image_str=file, hotel_id=hotel_id)
    process_pic.delay(file)
    return file
