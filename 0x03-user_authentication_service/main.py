#!/usr/bin/env python3

"""
Create a new module called main.py.
Create one function for each of the following tasks.
Use the requests module
to query your web server for the corresponding end-point.
Use assert to validate the response's expected status code
and payload (if any) for each task.
"""
import requests

BASE_URL = "http://127.0.0.1:5000"

def register_user(email: str, password: str) -> None:
    """Register a user and assert the response."""
    url = f"{BASE_URL}/users"
    response = requests.post(url, data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}

def log_in_wrong_password(email: str, password: str) -> None:
    """Try logging in with the wrong password."""
    url = f"{BASE_URL}/sessions"
    response = requests.post(url, data={"email": email, "password": password})
    assert response.status_code == 401

def log_in(email: str, password: str) -> str:
    """Log in the user and return the session_id."""
    url = f"{BASE_URL}/sessions"
    response = requests.post(url, data={"email": email, "password": password})
    assert response.status_code == 200
    session_id = response.cookies.get("session_id")
    assert session_id is not None
    return session_id

def profile_unlogged() -> None:
    """Try accessing the profile endpoint without being logged in."""
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403

def profile_logged(session_id: str) -> None:
    """Access the profile endpoint while logged in."""
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200

def log_out(session_id: str) -> None:
    """Log out the user and destroy the session."""
    url = f"{BASE_URL}/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200

def reset_password_token(email: str) -> str:
    """Request a password reset token for the user."""
    url = f"{BASE_URL}/reset_password"
    response = requests.post(url, data={"email": email})
    assert response.status_code == 200
    reset_token = response.json().get("reset_token")
    assert reset_token is not None
    return reset_token

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the user's password."""
    url = f"{BASE_URL}/reset_password"
    response = requests.put(url, data={"email": email, "reset_token": reset_token, "new_password": new_password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}

# Test the flow
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
