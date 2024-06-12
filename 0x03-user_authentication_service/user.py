#!/usr/bin/env python3
"""User model for SQLAlchemy database"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional

Base = declarative_base()


class User(Base):
    """SQLAlchemy data model for the users table"""
    __tablename__: str = 'users'
    id: Column = Column(Integer, primary_key=True)
    email: Column = Column(String(250), nullable=False)
    hashed_password: Column = Column(String(250), nullable=False)
    session_id: Column = Column(String(250), nullable=True)
    reset_token: Column = Column(String(250), nullable=True)

    def __str__(self) -> str:
        """Return the object as a string"""
        return "User<{}>".format(self.id)

    def __repr__(self) -> str:
        """Return the object representation"""
        return self.__str__()
