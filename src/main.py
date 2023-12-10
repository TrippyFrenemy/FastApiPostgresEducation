from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .contacts.router import router as router_contacts

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
    router_contacts,
    prefix="/contacts",
    tags=["Contacts"]
)
