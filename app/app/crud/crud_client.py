from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate


class CRUDUser(CRUDBase[Client, ClientCreate, ClientUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Client]:
        return db.query(Client).filter(Client.email == email).first()

    def create(self, db: Session, *, obj_in: ClientCreate) -> Client:
        db_obj = Client(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Client,
        obj_in: Union[ClientUpdate, Dict[str, Any]]
    ) -> Client:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[Client]:
        client = self.get_by_email(db, email=email)
        if not client:
            return None
        if not verify_password(password, client.hashed_password):
            return None
        return client


client = CRUDUser(Client)
