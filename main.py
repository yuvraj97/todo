from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT

from routs.auth_routes import auth_router
from routs.todo_routes import todo_router
from schemas.auth_schema import Settings


app = FastAPI()


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(auth_router)
app.include_router(todo_router)
