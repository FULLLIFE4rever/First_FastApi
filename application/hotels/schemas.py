from dataclasses import dataclass
from typing import List
from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict


@dataclass
class SHotelsCreate:

    name: str
    location: str

    image_id: UploadFile
    services: List[str] | None = None


class SHotelsInfo(SHotelsCreate):
    id: int
    image_id: str

    model_config = ConfigDict(from_attributes=True)
