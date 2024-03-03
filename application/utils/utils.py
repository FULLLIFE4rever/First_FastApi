import uuid

import aiofiles
from fastapi import UploadFile

from utils.exceptions import ConflictException


def filename_generator():
    return str(uuid.uuid4())


async def add_image(path: str, file: UploadFile):
    if not file.content_type.startswith("image"):
        raise ConflictException("Not image")
    name = f"{filename_generator()}.webp"
    path = f"{path}/{name}"
    async with aiofiles.open(
        f"/application/frontend/static/images/{path}",
        "wb+",
    ) as file_object:
        file = await file.read()
        await file_object.write(file)
    return path
