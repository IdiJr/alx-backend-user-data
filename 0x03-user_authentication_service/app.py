#!/usr/bin/env python3
"""
Flask app
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def hello() -> str:
    """GET route index

    Returns:
        str: JSON {'message': 'Bienvenue'}
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def user() -> str:
    """POST route for user registration

    Returns:
        str: Message
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "User created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
