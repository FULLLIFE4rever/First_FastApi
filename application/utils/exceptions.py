from fastapi import HTTPException, status


class ConflictException(HTTPException):
    def __init__(self, detail: str | None):
        status_code = status.HTTP_409_CONFLICT
        super().__init__(status_code=status_code, detail=detail)


class UnauthorizedException(HTTPException):
    def __init__(self, detail):
        status_code = status.HTTP_401_UNAUTHORIZED
        super().__init__(status_code=status_code, detail=detail)
