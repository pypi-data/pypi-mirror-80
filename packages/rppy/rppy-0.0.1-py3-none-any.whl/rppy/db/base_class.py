from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy_utils import UUIDType


def generate_uid():
    return uuid4()


class CustomBase(object):
    id = Column(Integer, primary_key=True)
    uid = Column(
        UUIDType,
        nullable=False,
        default=generate_uid
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False, nullable=False)

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=CustomBase)
