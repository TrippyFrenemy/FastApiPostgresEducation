from redis import asyncio as aioredis
from fastapi_limiter import FastAPILimiter
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .auth.base_config import fastapi_users
from .auth.schemas import UserRead, UserUpdate
from .config import REDIS_HOST, REDIS_PORT

from .contacts.router import router as router_contacts
from .auth.router import router as router_auth

app = FastAPI(title="Notes App")

# app.mount("/static", StaticFiles(directory="src/static"), name="static")

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],  # "GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"
    allow_headers=["*"]   # "Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                          # "Access-Control-Allow-Origin", "Authorization"
)
app.include_router(
    router_auth,
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=True),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    router_contacts,
    prefix="/contacts",
    tags=["Contacts"]
)


@app.on_event("startup")
async def startup():
    redis = aioredis.Redis(host=f"{REDIS_HOST}", port=int(f"{REDIS_PORT}"))
    await FastAPILimiter.init(redis)
