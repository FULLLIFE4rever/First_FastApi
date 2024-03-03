from datetime import datetime, timedelta, timezone

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, decode, encode
from passlib.context import CryptContext
from pydantic import EmailStr

from config import settings
from users.services import UsersService
from utils.exceptions import UnauthorizedException

SECRET_KEY = settings.SECRET_KEY.get_secret_value()
ALGORITHM = settings.SECRET_ALGORITHM.get_secret_value()

http_bearer = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def user_authentication(email: EmailStr, password: str):
    user = await UsersService.find_one_or_none(email=email)
    if not user:
        return
    return verify_password(password, user.hashed_password) and user


def create_access_token(
    data: dict, expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if not expires_delta:
        expires_delta = timedelta(minutes=30)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_payload(token: str):
    try:
        decoded = decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except ExpiredSignatureError:
        raise UnauthorizedException("Token error")
    return decoded


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    token = credentials.credentials
    return get_payload(token)
