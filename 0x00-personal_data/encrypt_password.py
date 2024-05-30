#!/usr/bin/env python3
"""Module to hash passwords using bcrypt"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted, hashed password.
    """
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check if a password is valid by comparing it to a hashed password.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The password to verify.

    Returns:
        bool: True if the password matches the
        hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
