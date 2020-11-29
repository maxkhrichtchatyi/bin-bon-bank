from typing import TYPE_CHECKING

from sqlalchemy import Column, Enum, ForeignKey, Integer, String

from app.core.consts import AccountTransactionType
from app.db.base_class import Base
from app.db.mixins import AuditMixin

if TYPE_CHECKING:
    from .client import Client  # noqa: F401


class AccountTransaction(Base, AuditMixin):
    __tablename__ = "account_transaction"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(AccountTransactionType), index=True)
    amount = Column(Integer, index=True, default=0)
    account_id = Column(Integer, ForeignKey("account.id"))
    uuid = Column(String(length=36), index=True)
