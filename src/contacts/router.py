import logging
from datetime import datetime, timedelta
from operator import and_

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, insert, or_, extract
from src.contacts.models import Contact
from src.contacts.schemas import ContactCreate, ContactInDB, ContactUpdate
from src.database import get_async_session

router = APIRouter()


@router.post("/contacts/", response_model=ContactInDB)
async def create_contact(contact: ContactCreate, db: AsyncSession = Depends(get_async_session)):
    new_contact = Contact(**contact.dict())
    db.add(new_contact)
    await db.commit()
    await db.refresh(new_contact)
    return new_contact


@router.get("/contacts/", response_model=list[ContactInDB])
async def read_contacts(db: AsyncSession = Depends(get_async_session)):
    query = select(Contact)
    result = await db.execute(query)
    contacts = result.scalars().all()
    return contacts


@router.get("/contacts/{contact_id}", response_model=ContactInDB)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_async_session)):
    query = select(Contact).where(Contact.id == contact_id)
    result = await db.execute(query)
    contact = result.scalar_one_or_none()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/contacts/{contact_id}", response_model=ContactInDB)
async def update_contact(contact_id: int, contact: ContactUpdate, db: AsyncSession = Depends(get_async_session)):
    query = select(Contact).where(Contact.id == contact_id)
    result = await db.execute(query)
    existing_contact = result.scalar_one_or_none()
    if existing_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    for key, value in contact.dict().items():
        setattr(existing_contact, key, value)
    db.add(existing_contact)
    await db.commit()
    await db.refresh(existing_contact)
    return existing_contact


@router.delete("/contacts/{contact_id}")
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_async_session)):
    query = select(Contact).where(Contact.id == contact_id)
    result = await db.execute(query)
    contact_to_delete = result.scalar_one_or_none()
    if contact_to_delete is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    await db.delete(contact_to_delete)
    await db.commit()
    return {"message": "Contact deleted successfully"}


@router.get("/search")
async def search_contacts(
        name: str = Query(None),
        surname: str = Query(None),
        email: str = Query(None),
        db: AsyncSession = Depends(get_async_session)
):
    logging.info(f"Received query parameters: name={name}, surname={surname}, email={email}")
    query_conditions = []

    if name:
        query_conditions.append(Contact.first_name.like(f"%{name}%"))
    if surname:
        query_conditions.append(Contact.last_name.like(f"%{surname}%"))
    if email:
        query_conditions.append(Contact.email.like(f"%{email}%"))

    query = select(Contact)
    if query_conditions:
        query = query.filter(or_(*query_conditions))

    result = await db.execute(query)
    contacts = result.scalars().all()
    return contacts


@router.get("/upcoming-birthdays")
async def upcoming_birthdays(db: AsyncSession = Depends(get_async_session)):
    current_date = datetime.now().date()
    upper_limit = current_date + timedelta(days=7)

    result = await db.execute(
        select(Contact).where(
            and_(
                extract('month', Contact.birthday) == current_date.month,
                extract('day', Contact.birthday).between(current_date.day, upper_limit.day)
            )
        )
    )
    contacts = result.scalars().all()
    return contacts
