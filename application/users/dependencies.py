from fastapi import Depends

from config import settings
from users.services import UsersService
from users.utils.auth import get_current_token_payload
from utils.exceptions import UnauthorizedException

SECRET_KEY = settings.SECRET_KEY.get_secret_value()
ALGORITHM = settings.SECRET_ALGORITHM.get_secret_value()


async def get_current_user(
    access_token: str = Depends(get_current_token_payload),
):
    user_email: str = access_token.get("sub")
    user = await UsersService.find_one_or_none(email=user_email)
    if not user:
        raise UnauthorizedException("The user has not been identified")
    return user


async def get_permission_user(
    access_token: str = Depends(get_current_token_payload),
):
    if access_token.get("auth") not in ("moderator", "admin"):
        raise UnauthorizedException("No details")
    return True
