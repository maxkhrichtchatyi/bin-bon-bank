from datetime import timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.tests.common.account import create_random_account, deposit_account
from app.tests.common.client import create_random_client


def test_create_account(
    test_client: TestClient, normal_client_token_headers: dict
) -> None:
    data = {"amount": 0, "currency": "USD"}
    response = test_client.post(
        f"{settings.API_V1_STR}/accounts/",
        headers=normal_client_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["amount"] == data["amount"]
    assert content["currency"] == data["currency"]
    assert "id" in content
    assert "client_id" in content


def test_read_account(test_client: TestClient, db: Session) -> None:
    account = create_random_account(db)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    a_token = security.create_access_token(
        account.client_id, expires_delta=access_token_expires
    )
    token = {"Authorization": f"Bearer {a_token}"}
    response = test_client.get(
        f"{settings.API_V1_STR}/accounts/{account.id}",
        headers=token,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["amount"] == account.amount
    assert content["currency"] == account.currency
    assert content["id"] == account.id
    assert content["client_id"] == account.client_id


def test_read_account_without_id(test_client: TestClient, db: Session) -> None:
    client = create_random_client(db)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    a_token = security.create_access_token(
        client.id, expires_delta=access_token_expires
    )
    token = {"Authorization": f"Bearer {a_token}"}
    response = test_client.get(
        f"{settings.API_V1_STR}/accounts/100000",
        headers=token,
    )
    assert response.status_code == 404


def test_read_account_enough_permissions(test_client: TestClient, db: Session) -> None:
    client = create_random_client(db)
    account = create_random_account(db)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    a_token = security.create_access_token(
        client.id, expires_delta=access_token_expires
    )
    token = {"Authorization": f"Bearer {a_token}"}
    response = test_client.get(
        f"{settings.API_V1_STR}/accounts/{account.id}",
        headers=token,
    )
    assert response.status_code == 400


def test_account_transfer(test_client: TestClient, db: Session) -> None:
    account = create_random_account(db)
    deposit_account(db, amount=100, account_id=account.id, client_id=account.client_id)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    a_token = security.create_access_token(
        account.client_id, expires_delta=access_token_expires
    )
    response = test_client.post(
        f"{settings.API_V1_STR}/accounts/transfer",
        headers={"Authorization": f"Bearer {a_token}"},
        json={
            "sender_account_id": account.id,
            "recipient_account_id": account.id,
            "amount": 10,
            "currency": "USD",
        },
    )
    assert response.status_code == 200
