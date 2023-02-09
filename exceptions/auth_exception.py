from fastapi.exceptions import HTTPException
from fastapi import status


class AuthExceptions:
    UNAUTHORIZED = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token"
    )
    USER_ALREADY_EXISTES = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="User with the email already exists"
    )
    AUTHENTICATION_DENIED = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid Username Or Password"
    )
    INVALID_REFRESH_TOKEN = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Please provide a valid refresh token daz"
    )

