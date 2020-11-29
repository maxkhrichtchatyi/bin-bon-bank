from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas import ClientCreate
from app.tests.common.fakers import random_email, random_lower_string


def test_get_access_token(test_client: TestClient, db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    client_in = ClientCreate(email=username, password=password)
    crud.client.create(db, obj_in=client_in)
    login_data = {
        "username": username,
        "password": password,
    }
    r = test_client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_get_access_token_incorrect_data(test_client: TestClient, db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    login_data = {
        "username": username,
        "password": password,
    }
    r = test_client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 400


def test_get_access_token_current_client(test_client: TestClient, db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    client_in = ClientCreate(email=username, password=password)
    crud.client.create(db, obj_in=client_in)
    login_data = {
        "username": username,
        "password": password,
    }
    r = test_client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert "token_type" in tokens
    assert tokens["access_token"]
    assert tokens["token_type"]
