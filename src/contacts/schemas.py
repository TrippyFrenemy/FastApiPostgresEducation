from pydantic import BaseModel
from typing import Optional
from datetime import date

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: Optional[date] = None
    additional_info: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass


class ContactInDB(ContactBase):
    id: int

    class Config:
        orm_mode = True
