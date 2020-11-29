from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql import func


@as_declarative()
class AuditMixin:
    @declared_attr
    def time_created(cls):
        return Column(DateTime(timezone=True), default=func.now())

    @declared_attr
    def time_updated(cls):
        return Column(DateTime(timezone=True), onupdate=func.now())
