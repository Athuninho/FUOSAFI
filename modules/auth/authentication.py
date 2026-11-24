"""
FUOSAFI - Authentication Manager
Handles user registration, authentication verification, and session state.
"""

from typing import Optional, Dict, Any, Tuple
import re
import config
from database.db import fetch_one, execute_query
from utils.security import hash_password, verify_password, validate_password_strength


def authenticate_user(email: str, password: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    """
    Authenticates a user by email and password.
    Returns: (is_authenticated, user_dict, error_message)
    """
    clean_email = email.strip().lower()
    if not clean_email or not password:
        return False, None, "Email and password are required."

    user = fetch_one("SELECT * FROM users WHERE LOWER(email) = ?;", (clean_email,))
    if not user:
        return False, None, "Invalid email or password."

    if user["account_status"] != "Active":
        return False, None, f"Account is {user['account_status'].lower()}. Please contact the administrator."

    if not verify_password(password, user["password_hash"]):
        return False, None, "Invalid email or password."

    # Success: sanitize output (remove sensitive password hash)
    user_data = dict(user)
    user_data.pop("password_hash", None)
    return True, user_data, ""


def register_user(
    full_name: str,
    email: str,
    phone_number: str,
    password: str,
    location: str,
    role: str = config.ROLE_RESIDENT
) -> Tuple[bool, Optional[int], str]:
    """
    Registers a new user in the database.
    Returns: (success, user_id, message)
    """
    clean_name = full_name.strip()
    clean_email = email.strip().lower()
    clean_phone = phone_number.strip()
    clean_location = location.strip()

    # Basic validations
    if not clean_name or len(clean_name) < 3:
        return False, None, "Please provide your full legal name."

    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, clean_email):
        return False, None, "Please enter a valid email address."

    is_strong, pwd_err = validate_password_strength(password)
    if not is_strong:
        return False, None, pwd_err

    if role not in config.USER_ROLES:
        return False, None, "Invalid account role selected."

    # Check if email is already taken
    existing = fetch_one("SELECT id FROM users WHERE LOWER(email) = ?;", (clean_email,))
    if existing:
        return False, None, "An account with this email address already exists."

    pwd_hash = hash_password(password)

    user_id = execute_query(
        """
        INSERT INTO users (full_name, email, phone_number, password_hash, role, location, account_status)
        VALUES (?, ?, ?, ?, ?, ?, 'Active');
        """,
        (clean_name, clean_email, clean_phone, pwd_hash, role, clean_location)
    )

    return True, user_id, "Registration successful! You may now log in."
