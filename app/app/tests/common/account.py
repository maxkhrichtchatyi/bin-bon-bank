from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.account import AccountCreate, AccountDeposit
from app.tests.common.client import create_random_client


def create_random_account(db: Session, currency: str = "USD") -> models.Account:
    client = create_random_client(db)
    account_in = AccountCreate(currency=currency, id=id)
    return crud.account.create(db=db, obj_in=account_in, client_id=client.id)


def deposit_account(
    db: Session, amount: int, client_id: int, account_id: int
) -> models.Account:
    account_in = AccountDeposit(amount=amount, account_id=account_id)
    return crud.account.deposit(db=db, obj_in=account_in, client_id=client_id)
