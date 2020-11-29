from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.core.security import verify_password
from app.schemas.client import ClientCreate, ClientUpdate
from app.tests.common.fakers import random_email, random_lower_string


def test_create_client(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    client_in = ClientCreate(email=email, password=password)
    client = crud.client.create(db, obj_in=client_in)
    assert client.email == email
    assert hasattr(client, "hashed_password")


def test_authenticate_client(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    client_in = ClientCreate(email=email, password=password)
    client = crud.client.create(db, obj_in=client_in)
    authenticated_client = crud.client.authenticate(db, email=email, password=password)
    assert authenticated_client
    assert client.email == authenticated_client.email


def test_not_authenticate_client(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    client = crud.client.authenticate(db, email=email, password=password)
    assert client is None


def test_get_client(db: Session) -> None:
    password = random_lower_string()
    username = random_email()
    client_in = ClientCreate(email=username, password=password, is_superuser=True)
    client = crud.client.create(db, obj_in=client_in)
    client_2 = crud.client.get(db, id=client.id)
    assert client_2
    assert client.email == client_2.email
    assert jsonable_encoder(client) == jsonable_encoder(client_2)


def test_update_client(db: Session) -> None:
    password = random_lower_string()
    email = random_email()
    client_in = ClientCreate(email=email, password=password)
    client = crud.client.create(db, obj_in=client_in)
    new_password = random_lower_string()
    client_in_update = ClientUpdate(password=new_password)
    crud.client.update(db, db_obj=client, obj_in=client_in_update)
    client_2 = crud.client.get(db, id=client.id)
    assert client_2
    assert client.email == client_2.email
    assert verify_password(new_password, client_2.hashed_password)


def test_update_client_exclude_unset(db: Session) -> None:
    password = random_lower_string()
    email = random_email()
    client_in = ClientCreate(email=email, password=password)
    client = crud.client.create(db, obj_in=client_in)
    new_password = random_lower_string()
    # client_in_update = ClientUpdate(password=new_password)
    crud.client.update(db, db_obj=client, obj_in=dict({"password": new_password}))
    client_2 = crud.client.get(db, id=client.id)
    assert client_2
    assert client.email == client_2.email
    assert verify_password(new_password, client_2.hashed_password)
