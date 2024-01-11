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



def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if the provided password matches the hashed password
    Args:
        hashed_password (bytes): hash
        password (str): password
    Returns:
        bool: true or false
    """
    if hashed_password and password:
        return bcrypt.checkpw(str.encode(password), hashed_password)
