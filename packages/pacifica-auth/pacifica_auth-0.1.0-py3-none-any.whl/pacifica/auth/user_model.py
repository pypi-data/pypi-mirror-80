#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Example user model for consumers to use."""
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

Base = declarative_base()


def _generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    """Example SQLAlchemy User Model."""

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(40), unique=True, default=_generate_uuid, index=True)
    username = Column(String(200))
    password = Column(String(200), default='')
    name = Column(String(100))
    email = Column(String(200))
    active = Column(Boolean, default=True)

    def is_active(self):
        """Return the user active attribute."""
        return self.active

    # pylint: disable=no-self-use
    def is_authenticated(self):
        """The user is always authenticated."""
        return True


__all__ = [
    'Base',
    'User'
]
