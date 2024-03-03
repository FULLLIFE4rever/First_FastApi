import asyncio
import json
import pprint
import re
from datetime import datetime

from httpx import AsyncClient
from pytest import fixture
from sqlalchemy import insert

from bookings.models import Bookings
from config import settings
from database import Base, async_session, engine
from hotels.models import Hotels
from hotels.rooms.models import Rooms
from main import app
from users.models import Users


@fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.TEST_MODE == True
    models_to_create = (Users, Hotels, Rooms, Bookings)
    for model in models_to_create:
        model.__name__.lower()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock(model: str):
        with open(f"tests/data/mock_{model}.json", encoding="UTF-8") as f:
            json_load = json.load(f)
            if model == "bookings":
                for i, item in enumerate(json_load):
                    item["date_from"] = datetime.strptime(
                        item["date_from"], "%Y-%m-%d"
                    )
                    item["date_to"] = datetime.strptime(
                        item["date_to"], "%Y-%m-%d"
                    )
            print(type(json_load))
            return json_load

    models = {}
    for model in models_to_create:
        models[model.__name__.lower()] = open_mock(model.__name__.lower())

    for model in models_to_create:
        async with async_session() as session:
            insert_to_table = insert(model).values(
                models.get(model.__name__.lower())
            )
            await session.execute(insert_to_table)
            await session.commit()


# @fixture(scope="session")
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@fixture(scope="function")
async def ac():
    "Асинхронный клиент для тестирования эндпоинтов"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@fixture(scope="session")
async def authenticated_ac():
    "Асинхронный аутентифицированный клиент для тестирования эндпоинтов"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/api/v1/auth/login",
            json={
                "email": "test@test.com",
                "password": "test",
            },
        )
        assert ac.cookies["booking_access_token"]
        yield ac
