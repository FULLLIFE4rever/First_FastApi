from typing import List

from fastapi import Request
from sqladmin.authentication import AuthenticationBackend

from users.router import login_user
from users.schemes import SUserAuth
from users.utils.auth import create_access_token, get_payload


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        user_data = SUserAuth(email=email, password=password)
        # Validate username/password credentials
        # And update session
        request.session.update({"Authorization": await login_user(user_data)})
        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("Authorization")
        if not token:
            return False
        auth = get_payload(token).get("auth")
        authority: List = ("admin", "moderator")
        if auth not in authority:
            return False
        return True


authentication_backend = AdminAuth(secret_key="")
