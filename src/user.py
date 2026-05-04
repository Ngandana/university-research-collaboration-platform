"""
user.py
Core User entity for the University Research Collaboration Platform.
Implements the User class from the Assignment 9 class diagram.
"""

from enum import Enum
from datetime import date
import hashlib


class UserRole(Enum):
    STUDENT = "STUDENT"
    SUPERVISOR = "SUPERVISOR"
    RESEARCHER = "RESEARCHER"
    ADMIN = "ADMIN"


class UserStatus(Enum):
    REGISTERED = "REGISTERED"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DEACTIVATED = "DEACTIVATED"


class User:
    """
    Represents a platform user.
    Roles: Student, Supervisor, Researcher, Admin.
    Status lifecycle: Registered → Active → Suspended/Deactivated.
    """

    def __init__(self, user_id: str, name: str, email: str,
                 password: str, role: UserRole):
        self._user_id = user_id
        self._name = name
        self._email = email
        self._password_hash = self._hash_password(password)
        self._role = role
        self._status = UserStatus.REGISTERED
        self._created_date = date.today()

    # ── Private helpers ───────────────────────────────────────────────────────
    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    # ── Getters ───────────────────────────────────────────────────────────────
    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def role(self) -> UserRole:
        return self._role

    @property
    def status(self) -> UserStatus:
        return self._status

    @property
    def created_date(self) -> date:
        return self._created_date

    # ── Methods ───────────────────────────────────────────────────────────────
    def register(self) -> None:
        """Email verified — activate account."""
        if self._status == UserStatus.REGISTERED:
            self._status = UserStatus.ACTIVE

    def login(self, password: str) -> bool:
        """Validate credentials. Returns True on success."""
        if self._status != UserStatus.ACTIVE:
            return False
        return self._password_hash == self._hash_password(password)

    def logout(self) -> None:
        """Terminate the user session (stateless stub)."""
        pass  # session management handled at service layer

    def update_profile(self, name: str = None, email: str = None) -> None:
        """Update name and/or email."""
        if self._status != UserStatus.ACTIVE:
            raise PermissionError("Only active users can update their profile.")
        if name:
            self._name = name
        if email:
            self._email = email

    def deactivate(self) -> None:
        """User deletes their account."""
        self._status = UserStatus.DEACTIVATED

    def suspend(self) -> None:
        """Admin suspends account due to violation."""
        if self._status == UserStatus.ACTIVE:
            self._status = UserStatus.SUSPENDED

    def reactivate(self) -> None:
        """Admin reactivates a suspended account."""
        if self._status == UserStatus.SUSPENDED:
            self._status = UserStatus.ACTIVE

    def get_role(self) -> UserRole:
        return self._role

    def get_status(self) -> UserStatus:
        return self._status

    def __repr__(self) -> str:
        return (f"User(id={self._user_id}, name={self._name}, "
                f"role={self._role.value}, status={self._status.value})")
