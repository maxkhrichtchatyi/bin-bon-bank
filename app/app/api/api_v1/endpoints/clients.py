from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Client)
def create_client(
    *,
    db: Session = Depends(deps.get_db),
    client_in: schemas.ClientCreate,
) -> Any:
    """
    Create new client.
    """
    client = crud.client.get_by_email(db, email=client_in.email)
    if client:
        raise HTTPException(
            status_code=400,
            detail="The client with this username already exists in the system.",
        )

    client = crud.client.create(db, obj_in=client_in)
    return client
