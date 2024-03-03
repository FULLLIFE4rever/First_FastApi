from fastapi import APIRouter, Depends, HTTPException, status

from users.dependencies import get_current_user
from users.models import Users
from users.schemes import SUserAuth, SUserInfo
from users.services import UsersService
from users.utils import get_password_hash, user_authentication
from users.utils.auth import create_access_token
from utils.exceptions import ConflictException

router_user = APIRouter(prefix="/auth", tags=["Авторизация и аутификация"])


@router_user.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: SUserAuth):
    user_exist = await UsersService.find_one_or_none(email=user.email)
    if user_exist:
        raise ConflictException("User already exists")
    hashed_password = get_password_hash(user.password)
    await UsersService.add(email=user.email, hashed_password=hashed_password)


@router_user.post("/login")
async def login_user(
    user_data: SUserAuth,
) -> str:
    user = await user_authentication(
        email=user_data.email, password=user_data.password
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token_data = {"sub": str(user.email), "auth": str(user.authority)}
    access_token = create_access_token(access_token_data)
    return access_token


@router_user.get("/me")
async def user_me(user: Users = Depends(get_current_user)) -> SUserInfo:
    return user


@router_user.get("/all")
async def users_all(
    user: Users = Depends(get_current_user),
) -> list[SUserInfo]:
    if user.email:
        return await UsersService.find_all()
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
