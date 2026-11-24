"""
FUOSAFI - Authentication Unit Tests
Tests registration, authentication logic, password hashing, and role verification.
"""

import pytest
import config
from modules.auth.authentication import authenticate_user, register_user
from database.db import fetch_one, execute_query

def test_successful_login():
    """Checks that seeded resident can authenticate properly."""
    success, user, msg = authenticate_user("resident@fuosafi.org", "ResidentPass123")
    assert success is True
    assert user is not None
    assert user["role"] == config.ROLE_RESIDENT
    assert "password_hash" not in user

def test_failed_login_bad_password():
    """Checks that invalid password fails."""
    success, user, msg = authenticate_user("resident@fuosafi.org", "WrongPassword!")
    assert success is False
    assert user is None
    assert "Invalid email or password" in msg

def test_failed_login_nonexistent_user():
    """Checks that non-existent email fails gracefully."""
    success, user, msg = authenticate_user("nonexistent@fuosafi.org", "Password123")
    assert success is False
    assert user is None

def test_user_registration_success():
    """Checks self-registration flow for new residents."""
    test_email = "test.resident.auto@fuosafi.org"
    # Ensure cleanup first
    execute_query("DELETE FROM users WHERE email = ?;", (test_email,))

    success, user_id, msg = register_user(
        full_name="Khadija Hassan",
        email=test_email,
        phone_number="+254700000000",
        password="SafePassword123",
        location="Tiwi Beach",
        role=config.ROLE_RESIDENT
    )
    assert success is True
    assert user_id is not None

    # Test login with new credentials
    auth_ok, user_data, _ = authenticate_user(test_email, "SafePassword123")
    assert auth_ok is True
    assert user_data["full_name"] == "Khadija Hassan"
    assert user_data["role"] == config.ROLE_RESIDENT

def test_user_registration_duplicate_email():
    """Checks that duplicate emails are rejected."""
    success, _, msg = register_user(
        full_name="Duplicate User",
        email="resident@fuosafi.org",
        phone_number="+254700000001",
        password="SafePassword123",
        location="Nyali",
        role=config.ROLE_RESIDENT
    )
    assert success is False
    assert "already exists" in msg

def test_weak_password_registration():
    """Checks that passwords shorter than 8 characters or lacking numbers are blocked."""
    success, _, msg = register_user(
        full_name="Weak Password User",
        email="weak@fuosafi.org",
        phone_number="+254700000002",
        password="short",
        location="Malindi",
        role=config.ROLE_RESIDENT
    )
    assert success is False
    assert "8 characters" in msg
