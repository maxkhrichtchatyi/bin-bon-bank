from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.db.mixins import AuditMixin

if TYPE_CHECKING:
    from .client import Client  # noqa: F401


class Account(Base, AuditMixin):
    __versioned__ = {}

    id = Column(Integer, primary_key=True, index=True)
    currency = Column(String, index=True)
    amount = Column(Integer, index=True, default=0)
    client_id = Column(Integer, ForeignKey("client.id"))
    client = relationship("Client", back_populates="accounts")
