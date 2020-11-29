from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Account)
def create_account(
    *,
    db: Session = Depends(deps.get_db),
    account_in: schemas.AccountCreate,
    current_client: models.Client = Depends(deps.get_current_client),
) -> Any:
    """
    Create new account.
    """
    account = crud.account.create(db=db, obj_in=account_in, client_id=current_client.id)
    return account


@router.get("/{id}", response_model=schemas.Account)
def read_account(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_client: models.Client = Depends(deps.get_current_client),
) -> Any:
    """
    Get account by ID.
    """
    account = crud.account.get(db=db, id=id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if account.client_id != current_client.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return account


@router.post("/transfer", response_model=schemas.Account)
def transfer_account_to_account(
    *,
    db: Session = Depends(deps.get_db),
    transfer_in: schemas.AccountTransfer,
    current_client: models.Client = Depends(deps.get_current_client),
) -> Any:
    """
    Create new transfer between accounts.
    """
    account = crud.account.transfer(
        db=db, obj_in=transfer_in, client_id=current_client.id
    )
    return account


@router.post("/deposit", response_model=schemas.Account)
def transfer_account_to_account(
    *,
    db: Session = Depends(deps.get_db),
    deposit_in: schemas.AccountDeposit,
    current_client: models.Client = Depends(deps.get_current_client),
) -> Any:
    """
    Contribution of money to your account.
    """
    account = crud.account.deposit(
        db=db, obj_in=deposit_in, client_id=current_client.id
    )
    return account
