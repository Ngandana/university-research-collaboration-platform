"""
services/user_service.py
Service layer for User business operations.

Responsibilities:
  - Validate inputs before passing to the repository.
  - Enforce business rules (e.g. unique email, role restrictions).
  - Coordinate between the domain model and the repository.
  - Raise descriptive exceptions so the API layer can return correct HTTP codes.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from typing import List, Optional
from src.user import User, UserRole, UserStatus
from repositories.interfaces import UserRepository
from creational_patterns.simple_factory import UserFactory


# ── Custom exceptions ─────────────────────────────────────────────────────────

class UserNotFoundError(Exception):
    def __init__(self, user_id: str):
        super().__init__(f"User '{user_id}' not found.")
        self.user_id = user_id


class DuplicateEmailError(Exception):
    def __init__(self, email: str):
        super().__init__(f"A user with email '{email}' already exists.")
        self.email = email


class InvalidRoleError(Exception):
    def __init__(self, role: str):
        super().__init__(
            f"Invalid role '{role}'. Valid roles: student, supervisor, researcher, admin."
        )


class UserNotActiveError(Exception):
    def __init__(self, user_id: str, status: str):
        super().__init__(f"User '{user_id}' is not active (status: {status}).")


# ── Service ───────────────────────────────────────────────────────────────────

class UserService:
    """
    Encapsulates all business logic relating to User management.
    Depends on UserRepository — injected at construction (Dependency Injection).
    """

    VALID_ROLES = {"student", "supervisor", "researcher", "admin"}

    def __init__(self, user_repository: UserRepository):
        self._repo = user_repository

    # ── Create ────────────────────────────────────────────────────────────────

    def register_user(self, user_id: str, name: str, email: str,
                      password: str, role: str) -> User:
        """
        Register a new user.
        Business rules:
          - Email must be unique across all users.
          - Role must be one of the valid values.
          - Password must be at least 6 characters.
        """
        if role.lower() not in self.VALID_ROLES:
            raise InvalidRoleError(role)

        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters.")

        if not name or not name.strip():
            raise ValueError("Name cannot be empty.")

        if not email or "@" not in email:
            raise ValueError("A valid email address is required.")

        if self._repo.find_by_email(email):
            raise DuplicateEmailError(email)

        if self._repo.exists(user_id):
            raise ValueError(f"User ID '{user_id}' is already in use.")

        user = UserFactory.create_user(user_id, name, email, password, role)
        user.register()   # immediately activate after email "verification"
        self._repo.save(user)
        return user

    # ── Read ──────────────────────────────────────────────────────────────────

    def get_user(self, user_id: str) -> User:
        """Return a user by ID or raise UserNotFoundError."""
        user = self._repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user

    def get_all_users(self) -> List[User]:
        """Return all registered users."""
        return self._repo.find_all()

    def get_users_by_role(self, role: str) -> List[User]:
        """Return all users with the specified role."""
        if role.lower() not in self.VALID_ROLES:
            raise InvalidRoleError(role)
        role_enum = UserRole[role.upper()]
        return self._repo.find_by_role(role_enum)

    # ── Update ────────────────────────────────────────────────────────────────

    def update_profile(self, user_id: str, name: str = None,
                       email: str = None) -> User:
        """
        Update a user's name and/or email.
        Business rules:
          - User must be ACTIVE.
          - New email must not already be taken by another user.
        """
        user = self.get_user(user_id)

        if user.status != UserStatus.ACTIVE:
            raise UserNotActiveError(user_id, user.status.value)

        if email and email != user.email:
            existing = self._repo.find_by_email(email)
            if existing and existing.user_id != user_id:
                raise DuplicateEmailError(email)

        user.update_profile(name=name, email=email)
        self._repo.save(user)
        return user

    # ── Delete / Status changes ───────────────────────────────────────────────

    def deactivate_user(self, user_id: str) -> User:
        """User requests account deletion."""
        user = self.get_user(user_id)
        user.deactivate()
        self._repo.save(user)
        return user

    def suspend_user(self, user_id: str) -> User:
        """Admin suspends a user account."""
        user = self.get_user(user_id)
        if user.status != UserStatus.ACTIVE:
            raise UserNotActiveError(user_id, user.status.value)
        user.suspend()
        self._repo.save(user)
        return user

    def reactivate_user(self, user_id: str) -> User:
        """Admin reactivates a suspended account."""
        user = self.get_user(user_id)
        if user.status != UserStatus.SUSPENDED:
            raise ValueError(f"User '{user_id}' is not suspended.")
        user.reactivate()
        self._repo.save(user)
        return user
