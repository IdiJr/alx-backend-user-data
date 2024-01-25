#!/usr/bin/env python3
"""
DB class
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:

    def __init__(self):
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database

        Args:
            email (string): email of user
            hashed_password (string): password of user
        Returns:
            User: user created
        """
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user
    

    def find_user_by(self, **kwargs) -> User:
        """Find a user by given filter arguments
        Returns:
            User: Found User object
        Raises:
            NoResultFound: When no results are found
            InvalidRequestError: When wrong query arguments are passed
        """
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user