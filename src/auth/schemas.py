from datetime import datetime

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    email: str


class UserCreate(schemas.BaseUserCreate):
    email: str


class UserUpdate(schemas.BaseUserUpdate):
    email: str