import asyncio
import unittest
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.config import DB_USER_TEST, DB_PASS_TEST, DB_HOST_TEST, DB_PORT_TEST, DB_NAME_TEST
from src.database import get_async_session, metadata
from src.contacts.models import Contact
from src.main import app

# DATABASE
DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


class TestContactAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_create_contact(self):
        data = {"name": "John Doe", "email": "john@example.com"}
        response = self.client.post("/contacts/", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], data["name"])
        self.assertEqual(response.json()["email"], data["email"])

    def test_read_contacts(self):
        # Populate the database with test data
        with async_session() as db:
            contact = Contact(name="Alice", email="alice@example.com")
            db.add(contact)
            db.commit()

        response = self.client.get("/contacts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["name"], "Alice")
        self.assertEqual(response.json()[0]["email"], "alice@example.com")


if __name__ == "__main__":
    unittest.main()
