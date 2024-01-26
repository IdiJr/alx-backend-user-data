#!/usr/bin/env python3
"""
Auth module
"""
from db import DB
from uuid import uuid4
from user import User
from bcrypt import hashpw, gensalt, checkpw
from typing import TypeVar
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """Hash a password for a user.

    Args:
        password (str): User's password.

    Returns:
        str: Hashed password.
    """
    return hashpw(password.encode('utf-8'), gensalt())
