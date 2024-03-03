import aioredis
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqladmin import Admin

from admin.auth import authentication_backend
from admin.views import (
    BookingAdmin,
    HotelAdmin,
    RoomAdmin,
    UserAdmin,
)
from bookings.routers import bookings_router
from config import settings, BASE_DIR
from database import engine
from frontend.pages.pages import frontend_router
from hotels.routers import hotels_router
from images.router import image_router
from users.router import router_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    # при запуске
    redis = aioredis.from_url(
        settings.redis_url,
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(
    title="API_NAME",
    description="API_DESC",
    docs_url="/api/docs",
    redoc_url=None,
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)
# STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
# app.mount("/static", StaticFiles(directory=STATIC_ROOT), "static")
app.mount("/static", StaticFiles(directory="./frontend/static"), "static")
app.mount("/images", StaticFiles(directory=BASE_DIR / "images"), "images")
origins = ["*"]


ALLOW_METHODS = ("DELETE", "GET", "PATCH", "POST", "PUT")
ALLOW_HEADERS = (
    "Content-Type",
    "Set-Cookie",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Origin",
    "Authorization",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADERS,
)
app.include_router(router_user, prefix="/api/v1")
app.include_router(bookings_router, prefix="/api/v1")
app.include_router(hotels_router, prefix="/api/v1")
app.include_router(image_router, prefix="/api/v1")
app.include_router(frontend_router)


admin = Admin(
    app,
    engine,
    authentication_backend=authentication_backend,
    base_url="/api/admin",
)
admin.add_view(UserAdmin)

admin.add_view(BookingAdmin)
admin.add_view(HotelAdmin)
admin.add_view(RoomAdmin)
