import uuid
from typing import List

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.consts import AccountTransactionType
from app.crud.base import CRUDBase
from app.models.account import Account
from app.models.account_transaction import AccountTransaction
from app.schemas.account import (
    AccountCreate,
    AccountDeposit,
    AccountTransfer,
    AccountUpdate,
)


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    def create(self, db: Session, *, obj_in: AccountCreate, client_id: int) -> Account:
        transaction_uuid = str(uuid.uuid4())

        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, client_id=client_id)
        db.add(db_obj)
        db.flush()

        db_obj_account_transaction = AccountTransaction(
            type=AccountTransactionType.create,
            account_id=db_obj.id,
            amount=0,
            uuid=transaction_uuid,
        )
        db.add(db_obj_account_transaction)
        db.flush()

        db.commit()
        db.refresh(db_obj)

        return db_obj

    def get_by_client(self, db: Session, *, client_id: int) -> List[Account]:
        return db.query(self.model).filter(Account.client_id == client_id).first()

    def transfer(
        self, db: Session, *, obj_in: AccountTransfer, client_id: int
    ) -> Account:
        transaction_uuid = str(uuid.uuid4())

        db_obj_account = (
            db.query(self.model)
            .with_for_update()
            .filter(Account.id == obj_in.sender_account_id)
            .first()
        )

        if db_obj_account.amount < obj_in.amount:
            raise HTTPException(status_code=400, detail="Not enough money")

        if db_obj_account.client_id != client_id:
            raise HTTPException(status_code=400, detail="Not enough permissions")

        db_obj_account.amount -= obj_in.amount
        db.add(db_obj_account)
        db.flush()

        db_obj_recipient_account = (
            db.query(self.model)
            .with_for_update()
            .filter(self.model.id == obj_in.recipient_account_id)
            .first()
        )

        db_obj_recipient_account.amount += obj_in.amount
        db.add(db_obj_recipient_account)
        db.flush()

        db_obj_account_transaction = AccountTransaction(
            type=AccountTransactionType.withdraw,
            account_id=obj_in.sender_account_id,
            amount=obj_in.amount,
            uuid=transaction_uuid,
        )
        db.add(db_obj_account_transaction)
        db.flush()

        db_obj_account_transaction = AccountTransaction(
            type=AccountTransactionType.deposit,
            account_id=obj_in.recipient_account_id,
            amount=obj_in.amount,
            uuid=transaction_uuid,
        )
        db.add(db_obj_account_transaction)
        db.flush()

        db.commit()
        db.refresh(db_obj_account)

        return db_obj_account

    def deposit(
        self, db: Session, *, obj_in: AccountDeposit, client_id: int
    ) -> Account:
        transaction_uuid = str(uuid.uuid4())

        db_obj_account = (
            db.query(self.model)
            .with_for_update()
            .filter(Account.id == obj_in.account_id)
            .first()
        )

        if db_obj_account.client_id != client_id:
            raise HTTPException(status_code=400, detail="Not enough permissions")

        db_obj_account.amount += obj_in.amount
        db.add(db_obj_account)
        db.flush()

        db_obj_account_transaction = AccountTransaction(
            type=AccountTransactionType.deposit,
            account_id=obj_in.account_id,
            amount=obj_in.amount,
            uuid=transaction_uuid,
        )
        db.add(db_obj_account_transaction)
        db.flush()

        db.commit()
        db.refresh(db_obj_account)

        return db_obj_account


account = CRUDAccount(Account)
