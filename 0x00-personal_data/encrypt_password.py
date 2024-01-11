#!/usr/bin/env python3
"""
encrypt_passwaords module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes and salts a password using bcrypt
    Args:
        password (str): password
    Returns:
        bytes: encryption password
    """
    hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
    if password:
        return hashed_password
