from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.db.mixins import AuditMixin

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class Client(Base, AuditMixin):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    accounts = relationship("Account", uselist=False, back_populates="client")
