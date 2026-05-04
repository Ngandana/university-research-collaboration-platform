"""
simple_factory.py
Pattern: Simple Factory
──────────────────────────────────────────────────────────────────────────────
Use case: Centralised User creation.

A UserFactory creates the correct User object based on a role string, so
callers never need to know which constructor arguments differ per role.
This maps directly to FR2 (Role-Based Access Control) — the system must
produce users with pre-set roles without exposing construction details.
"""

from src.user import User, UserRole


class UserFactory:
    """
    Simple Factory — single static method returns a fully configured User.

    Why Simple Factory here:
        All User objects share the same class; only the role enum value varies.
        A simple factory with a role-dispatch is the lightest-weight solution.
        There is no need to subclass User per role (that would be over-engineering).
    """

    @staticmethod
    def create_user(user_id: str, name: str, email: str,
                    password: str, role: str) -> User:
        """
        Create and return a User with the requested role.

        Args:
            user_id:  Unique identifier string.
            name:     Full display name.
            email:    Email address.
            password: Plain-text password (hashed internally).
            role:     One of 'student', 'supervisor', 'researcher', 'admin'.

        Returns:
            A User instance in REGISTERED status.

        Raises:
            ValueError: If role string is unrecognised.
        """
        role_map = {
            "student":    UserRole.STUDENT,
            "supervisor": UserRole.SUPERVISOR,
            "researcher": UserRole.RESEARCHER,
            "admin":      UserRole.ADMIN,
        }

        role_key = role.lower().strip()
        if role_key not in role_map:
            raise ValueError(
                f"Unknown role '{role}'. "
                f"Valid roles: {list(role_map.keys())}"
            )

        return User(
            user_id=user_id,
            name=name,
            email=email,
            password=password,
            role=role_map[role_key],
        )


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    student = UserFactory.create_user("u1", "Alice Dube", "alice@uni.ac.za",
                                      "pass123", "student")
    supervisor = UserFactory.create_user("u2", "Prof Nkosi", "nkosi@uni.ac.za",
                                        "securepass", "supervisor")
    print(student)
    print(supervisor)
