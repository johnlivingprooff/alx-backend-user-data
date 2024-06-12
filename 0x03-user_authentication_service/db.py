#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound, InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database and return the User object
        """
        if not email or not hashed_password:
            raise ValueError("Email and hashed_password must be provided")

        # Check if the user already exists
        existing_user = self._session.query(User).filter_by(
                                                            email=email
                                                            ).first()
        if existing_user:
            raise ValueError(f"User with email {email} already exists")

        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception as e:
            self._session.rollback()  # Rollback the session in case of error
            raise e

        return new_user
    
    def find_user_by(self, **kwargs) -> User:
        """Find a user by a given attribute
        """
        if not kwargs:
            raise InvalidRequestError("No attribute provided")

        try:
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found with the provided attribute")
        return user
