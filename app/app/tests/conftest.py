from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.main import app
from app.tests.common.client import authentication_token_from_email


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def test_client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def normal_client_token_headers(test_client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_email(
        test_client=test_client, email=settings.EMAIL_TEST_USER, db=db
    )
