import enum


class AccountTransactionType(enum.Enum):
    create = 1
    deposit = 2
    withdraw = 3
