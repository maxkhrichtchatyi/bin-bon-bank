from pydantic import BaseModel


# Shared properties
class AccountBase(BaseModel):
    amount: int


# Properties to receive via API on creation
class AccountCreate(BaseModel):
    currency: str = "USD"


# Properties to receive via API on deposit
class AccountDeposit(AccountBase):
    account_id: int


# Properties to receive via API on transfer money
class AccountTransfer(AccountBase, AccountCreate):
    sender_account_id: int
    recipient_account_id: int


# Properties to receive via API on update
class AccountUpdate(AccountBase):
    pass


# Properties shared by models stored in DB
class AccountInDBBase(AccountBase):
    id: int
    client_id: int
    currency: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class Account(AccountInDBBase):
    pass
