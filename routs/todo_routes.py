from datetime import datetime

from fastapi import APIRouter, status, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

from database import collection
from decorators.auth import auth_handler
from schemas.todo_schema import TodoPut, TodoUpdate, TodoDelete

todo_router = APIRouter(
    prefix='/todo',
)


def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds() * 1000.0)


@todo_router.put('/', status_code=status.HTTP_201_CREATED)
@auth_handler
def put_todo(todo: TodoPut, Authorize: AuthJWT = Depends()):
    email = Authorize.get_jwt_subject()
    entry = dict(
        email=email,
        type="todo",
        id=unix_time_millis(datetime.utcnow()),
        header=todo.header,
        description=todo.description
    )
    collection.insert_one(entry)
    return True


@todo_router.get('/', status_code=status.HTTP_200_OK)
@auth_handler
# Need to apply pagination (cursor approach for lazy loading)
# return sorted todos
def get_todo(Authorize: AuthJWT = Depends()):
    email = Authorize.get_jwt_subject()
    todo = collection.find(dict(
        email=email,
        type="todo",
        # id=cursor_key
    ))
    todo = [data for data in todo]
    for data in todo: del data["_id"]
    return jsonable_encoder(todo)


@todo_router.put('/update', status_code=status.HTTP_201_CREATED)
@auth_handler
def put_todo_update(todo: TodoUpdate, Authorize: AuthJWT = Depends()):
    email = Authorize.get_jwt_subject()
    # update only required fields
    # fetch -> modify -> update
    collection.update_one(
        dict(
            email=email,
            type="todo",
            id=todo.id,
        ),
        {
            "$set": dict(
                header=todo.header,
                description=todo.description
            )
        }
    )
    return True


@todo_router.delete('/', status_code=status.HTTP_202_ACCEPTED)
@auth_handler
def delete_todo(todo: TodoDelete, Authorize: AuthJWT = Depends()):
    collection.delete_one(dict(id=todo.id))
    return True
