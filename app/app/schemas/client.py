from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class ClientBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


# Properties to receive via API on creation
class ClientCreate(ClientBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class ClientUpdate(ClientBase):
    password: Optional[str] = None


# Properties shared by models stored in DB
class ClientInDBBase(ClientBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Client(ClientInDBBase):
    pass


# Additional properties stored in DB
class ClientInDB(ClientInDBBase):
    hashed_password: str
