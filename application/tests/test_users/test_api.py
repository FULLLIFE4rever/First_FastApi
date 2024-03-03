from fastapi import status
from httpx import AsyncClient
from pytest import mark


@mark.parametrize(
    "email,password,status_code",
    [
        ("kot@pes.com", "kotopes", status.HTTP_201_CREATED),
        ("kot@pes.com", "kot0pes", status.HTTP_409_CONFLICT),
        ("pes@kot.com", "pesokot", status.HTTP_201_CREATED),
        ("abcde", "pesokot", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert (
        response.status_code == status_code,
    ), f"Ошибка: статус {response.status_code}"


@mark.parametrize(
    "email,password,status_code",
    [
        ("test@test.com", "test", 200),
        ("artem@example.com", "artem", 200),
        ("wrong@person.com", "artem", 401),
    ],
)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert (
        response.status_code == status_code
    ), f"Ошибка: статус {response.status_code}"
