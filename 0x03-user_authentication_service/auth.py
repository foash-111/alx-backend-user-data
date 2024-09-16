#!/usr/bin/env python3
"""
hashing password file
"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str = "", password: str = "") -> User:
        """store user with hashed password"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            password = _hash_password(password)
            new_user = self._db.add_user(email, password)
            return new_user

    def valid_login(self, email: str = "", password: str = "") -> bool:
        try:
            current_user = self._db.find_user_by(email=email)
            if current_user:
                if bcrypt.checkpw(password.encode(),
                                  current_user.hashed_password):
                    return True
                return False
        except NoResultFound:
            return False

    def create_session(self, email=""):
        """create session to the corresponding User or None"""
        current = self._db.find_user_by(email=email)
        if current:
            current.session_id = _generate_uuid()
            self._db.update_user(user_id=current.id)
            return current.session_id
        return None

    def get_user_from_session_id(self, session_id=""):
        """returns the corresponding User or None"""
        if session_id:
            cur_user = self._db.find_user_by(session_id=session_id)
            if cur_user:
                return cur_user
            return None
        return None

    def destroy_session(self, user_id=0):
        cur_user = self._db.find_user_by(id=user_id)
        cur_user.session_id = None
        self._db.update_user(user_id=cur_user.id)
        return None

    def get_reset_password_token(self, email=""):
        """get_reset_password_token"""
        if email:
            user = self._db.find_user_by(email=email)
            if user:
                user.reset_token = _generate_uuid()
                self._db.update_user(user_id=user.id)
                return user.reset_token
            else:
                raise ValueError

    def update_password(self, reset_token="", password=""):
        user = self._db.find_user_by(reset_token=reset_token)
        if user:
            user.hashed_password = _hash_password(password)
            user.reset_token = None
            self._db.update_user(user_id=user.id)
            return None
        else:
            raise ValueError


def _hash_password(password: str = "") -> bytes:
    """
    >>> 'str'.encode()
    b'str'
    """
    password = password.encode()  # to transform it into bytes
    salt = bcrypt.gensalt()  # (add randomness to the hash)

    return bcrypt.hashpw(password, salt)


def _generate_uuid():
    """generate uuid and return it as a str representation"""
    return str(uuid4())
