#!/usr/bin/env python3

"""
Create a new module called main.py.
Create one function for each of the following tasks.
Use the requests module
to query your web server for the corresponding end-point.
Use assert to validate the response's expected status code
and payload (if any) for each task.
"""
from auth import Auth
from user import User
import requests
from flask import jsonify

AUTH = Auth()


def register_user(email: str, password: str) -> None:
    data = {'email': email, 'password': password}
    response = requests.post('0.0.0.0:5000/users', data=data)
    try:
        user = AUTH.register_user(email, password)
        expected = jsonify({"email": f"{email}", "message": "user created"}), 200
        assert response == expected
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400

def log_in_wrong_password(email: str, password: str) -> None:
    AUTH.valid_login(email, password)

def log_in(email: str, password: str) -> str:
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email=email)
        return session_id

def profile_unlogged() -> None:
    user = AUTH._db._session.query(User).filter_by(email=EMAIL).first()
    if user:
        if user.session_id:
            AUTH.destroy_session(user_id=user.id)
            return None
           
def profile_logged(session_id: str) -> None:
     if session_id:
            cur_user = AUTH._db._session.query(User).filter_by(session_id=session_id).first()
            if cur_user:
                return cur_user

def log_out(session_id: str) -> None
def reset_password_token(email: str) -> str
def update_password(email: str, reset_token: str, new_password: str) -> None

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
