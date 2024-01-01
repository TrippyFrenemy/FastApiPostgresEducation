from fastapi import APIRouter

from .base_config import auth_backend, fastapi_users
from .schemas import UserRead, UserCreate, UserUpdate


router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="",
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="",
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="",
    tags=["Auth"],
)

