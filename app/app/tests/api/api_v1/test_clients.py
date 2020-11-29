from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas import ClientCreate
from app.tests.common.fakers import random_email, random_lower_string


def test_create_user_new_email(
    test_client: TestClient, normal_client_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = test_client.post(
        f"{settings.API_V1_STR}/clients/",
        headers=normal_client_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_client = r.json()
    client = crud.client.get_by_email(db, email=username)
    assert client
    assert client.email == created_client["email"]


def test_create_client_existing_username(
    test_client: TestClient, normal_client_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = ClientCreate(email=username, password=password)
    crud.client.create(db, obj_in=user_in)
    data = {"email": username, "password": password}
    r = test_client.post(
        f"{settings.API_V1_STR}/clients/",
        headers=normal_client_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_create_client_by_normal_client(
    test_client: TestClient, normal_client_token_headers: Dict[str, str]
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = test_client.post(
        f"{settings.API_V1_STR}/clients/",
        headers=normal_client_token_headers,
        json=data,
    )
    assert r.status_code == 200
