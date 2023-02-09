import datetime
import traceback

from fastapi import APIRouter, status, Depends
from fastapi_jwt_auth.exceptions import MissingTokenError, InvalidHeaderError
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from werkzeug.security import generate_password_hash, check_password_hash

from database import collection
from exceptions.auth_exception import AuthExceptions
from decorators.auth import auth_handler
from schemas.auth_schema import SignUpModel, LoginModel

auth_router = APIRouter(
    prefix='/auth',
)
access_token_expires_time = datetime.timedelta(days=3)
refresh_token_expires_time = datetime.timedelta(days=30)


@auth_router.get('/')
@auth_handler
def get_auth_root(Authorize: AuthJWT = Depends()):
    return {"message": "Hello World"}


@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
def post_signup(user: SignUpModel):
    db_user = collection.find_one({
        "email": user.email,
        "type": "users"
    })

    if db_user is not None:
        return AuthExceptions.USER_ALREADY_EXISTES
    new_user = dict(
        type="users",
        email=user.email,
        password=generate_password_hash(user.password),
        role=user.role,
    )
    collection.insert_one(new_user)
    return True


@auth_router.post('/login', status_code=200)
def post_login(user: LoginModel, Authorize: AuthJWT = Depends()):
    db_user = collection.find_one({
        "email": user.email,
        "type": "users"
    })

    if db_user and check_password_hash(db_user["password"], user.password):
        access_token = Authorize.create_access_token(subject=db_user["email"], expires_time=access_token_expires_time)
        refresh_token = Authorize.create_refresh_token(subject=db_user["email"], expires_time=refresh_token_expires_time)
        response = {
            "access": access_token,
            "refresh": refresh_token
        }
        return jsonable_encoder(response)
    raise AuthExceptions.AUTHENTICATION_DENIED


@auth_router.get('/refresh')
def get_refresh_token(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except (InvalidHeaderError, MissingTokenError):
        traceback.print_exc()
        raise AuthExceptions.INVALID_REFRESH_TOKEN
    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=current_user, expires_time=access_token_expires_time)
    return jsonable_encoder({"access": access_token})
