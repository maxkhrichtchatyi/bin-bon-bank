from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate
from app.tests.common.fakers import random_email, random_lower_string


def client_authentication_headers(
    *, test_client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}
    r = test_client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_client(db: Session) -> Client:
    email = random_email()
    password = random_lower_string()
    client_in = ClientCreate(username=email, email=email, password=password)
    client = crud.client.create(db=db, obj_in=client_in)
    return client


def authentication_token_from_email(
    *, test_client: TestClient, email: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the client with given email.
    If the client doesn't exist it is created first.
    """
    password = random_lower_string()
    client_obj = crud.client.get_by_email(db, email=email)
    if not client_obj:
        client_in_create = ClientCreate(username=email, email=email, password=password)
        client_obj = crud.client.create(db, obj_in=client_in_create)
    else:
        client_in_update = ClientUpdate(password=password)
        client_obj = crud.client.update(db, db_obj=client_obj, obj_in=client_in_update)

    return client_authentication_headers(
        test_client=test_client, email=email, password=password
    )
