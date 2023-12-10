# Contact Management REST API

This project is a REST API for managing contact information, built using FastAPI and SQLAlchemy with PostgreSQL as the database backend. It allows for creating, retrieving, updating, and deleting contact details, as well as searching contacts and fetching contacts with upcoming birthdays.

## Features

- CRUD operations: Create, Read, Update, Delete contacts.
- Search contacts by name, surname, or email.
- Get contacts with birthdays in the next 7 days.
- PostgreSQL database integration.
- Asynchronous request handling.
- Pydantic models for data validation.
- Auto-generated API documentation using Swagger UI.

## Technologies

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.7+.
- **SQLAlchemy**: The Python SQL Toolkit and Object-Relational Mapper.
- **PostgreSQL**: An open-source relational database.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **asyncpg**: A database interface library designed specifically for PostgreSQL and Python/asyncio.

## Getting Started

### Prerequisites

- Python 3.7+
- PostgreSQL

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/TrippyFrenemy/FastApiPostgresEducation.git
   ```
2. Navigate to the project directory:
   ```sh
   cd FastApiPostgresEducation
   ```
3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

### Setting up the Database

- Ensure PostgreSQL is installed and running.
- Create a new PostgreSQL database for the project.
- Update the database connection details in `config.py`.

### Running the Application

1. Start the FastAPI server:
   ```sh
   uvicorn src.main:app --reload
   ```
2. Access the Swagger UI documentation at `http://127.0.0.1:8000/docs`.

## Usage

The API supports the following operations:

- **Create a Contact**: `POST /contacts/`
- **List all Contacts**: `GET /contacts/`
- **Retrieve a Contact by ID**: `GET /contacts/{contact_id}`
- **Update a Contact**: `PUT /contacts/{contact_id}`
- **Delete a Contact**: `DELETE /contacts/{contact_id}`
- **Search Contacts**: `GET /contacts/search?name=...&surname=...&email=...`
- **Contacts with Upcoming Birthdays**: `GET /contacts/upcoming-birthdays`

Refer to the Swagger UI documentation for more details on request and response formats.
