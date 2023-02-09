from pydantic import BaseModel
from typing import Optional


class TodoPut(BaseModel):
    # id: int
    header: str
    description: str = ""


class TodoUpdate(BaseModel):
    id: int
    header: str
    description: str


class TodoDelete(BaseModel):
    id: int
