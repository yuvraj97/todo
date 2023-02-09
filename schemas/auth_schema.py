from pydantic import BaseModel
from typing import Optional
from config import AUTH_JWT_SECRET_KEY


class Settings(BaseModel):
    authjwt_secret_key: str = AUTH_JWT_SECRET_KEY


class LoginModel(BaseModel):
    email: str
    password: str


class SignUpModel(BaseModel):
    email: str
    password: str
    role: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "email": "yuvraj@quantml.org",
                "password": "password",
                "role": "admin",  # should be enum
            }
        }
