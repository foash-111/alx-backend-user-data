#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        # echo=False (default) (no SQL logs will be shown)
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

    def add_user(self, email: str = "", hashed_password: str = "") -> User:
        """add new user from User class and store it"""
        if email and hashed_password:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
            return new_user
        return None

    def find_user_by(self, **kwargs) -> User:
        """query the first matched email"""
        for key, value in kwargs.items():
            if User.__dict__.get(key):
                current_user = self._session.query(User).\
                    filter_by(**kwargs).first()
                if current_user:
                    return current_user
                else:
                    raise NoResultFound
            raise InvalidRequestError

    def update_user(self, user_id: int = 0, **kwargs) -> None:
        """update user by its matched id"""
        try:
            user = self.find_user_by(id=user_id)
            # print(user.__dict__)
            for key, value in kwargs.items():
                # if user.__dict__.get(key):
                #     user.__dict__[key] = value
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError
            self._session.commit()
            return None
        except NoResultFound:
            raise ValueError
