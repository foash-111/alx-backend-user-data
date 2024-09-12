#!/usr/bin/env python3
"""
my base flask module
"""

from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth, _hash_password
from user import User


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['GET', 'POST'])
def users():
    """register new user"""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['GET', 'POST'])
def login():
    """create session for logged user"""
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email=email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    Find the user with the requested session ID.
    If the user exists destroy the session and redirect the user to GET /.
    If the user does not exist, respond with a 403 HTTP status.
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH._db._session.query(User).\
            filter_by(session_id=session_id).first()
        if user:
            AUTH.destroy_session(user_id=user.id)
            return redirect(url_for('home'))
        else:
            abort(403)
    else:
        return "the request doesn't contain session_id\n", 400


@app.route('/profile')
def profile():
    """get user profile if session_id exists"""
    session_id = request.cookies.get('session_id')
    user = AUTH._db._session.query(User).\
        filter_by(session_id=session_id).first()
    if user:
        return jsonify({"email": f"{user.email}"})
    abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """reset password using email and respond with reset_token"""
    email = request.form.get('email')
    user = AUTH._db._session.query(User).filter_by(email=email).first()
    if email:
        user.reset_token = AUTH.get_reset_password_token(email=email)
        AUTH._db._session.commit()
        return jsonify({"email": f"{user.email}",
                        "reset_token": f"{user.reset_token}"}), 200
    else:
        abort(403)


@app.route('/update_password', methods=['PUT'])
def update_password():
    """update password from form data tested using curl -d, not url args"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    user = AUTH._db._session.query(User).filter_by(email=email).first()
    if user:
        if user.reset_token == reset_token:
            user.hashed_password = _hash_password(new_password)
            AUTH._db._session.commit()
        else:
            abort(403)
        return jsonify(
            {"email": f"{user.email}", "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
