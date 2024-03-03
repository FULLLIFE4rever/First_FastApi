from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from hotels.routers import get_hotels

frontend_router = APIRouter(tags=["Frontend"])

templates = Jinja2Templates(directory="frontend/templates")


@frontend_router.get("/hotels")
def get_hotels_page(request: Request, hotels=Depends(get_hotels)):
    return templates.TemplateResponse(
        "index.html", {"request": request, "hotels": hotels}
    )
