from sqlalchemy.orm import configure_mappers

from .account import Account
from .account_transaction import AccountTransaction
from .client import Client

configure_mappers()
