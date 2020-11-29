import pytest
from fastapi.exceptions import HTTPException
from jose import jwt
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import crud
from app.api.deps import get_current_client
from app.core import security
from app.core.config import settings
from app.schemas import ClientCreate
from app.tests.common.fakers import random_email, random_lower_string


def test_get_current_client(test_client: TestClient, db: Session):
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

    client = get_current_client(db, tokens["access_token"])
    assert client.email == client_in.email


def test_get_current_client_not_found(db: Session):
    payload = jwt.encode(
        {"some": "data"}, settings.SECRET_KEY, algorithm=security.ALGORITHM
    )
    with pytest.raises(HTTPException):
        get_current_client(db, payload)


def test_get_current_client_not_validate_credentials(db: Session):
    with pytest.raises(HTTPException):
        get_current_client(db, "")
