#!/usr/bin/env python3
"""
Session Authentication module.
"""
from flask import Flask, request, jsonify, make_response
from api.v1.views import app_views
from models.user import User
from os import getenv

app = Flask(__name__)


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """ Handle Session Authentication login.

    Returns:
        JSON response.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return make_response(jsonify({"error": "email missing"}), 400)

    if not password:
        return make_response(jsonify({"error": "password missing"}), 400)

    user = User.search({'email': email})
    
    if not user:
        return make_response(jsonify({"error": "no user found for this email"}), 404)

    if not user[0].is_valid_password(password):
        return make_response(jsonify({"error": "wrong password"}), 401)

    auth = app.auth.create_session(user[0].id)
    user_dict = user[0].to_json()
    response = make_response(jsonify(user_dict))
    response.set_cookie(getenv('SESSION_NAME'), auth)

    return response
