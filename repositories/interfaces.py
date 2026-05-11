"""
interfaces.py
Repository interface definitions for the University Research Collaboration Platform.

Design decisions:
- A single generic Repository[T, ID] base interface avoids duplicating CRUD
  signatures across every entity repository.
- Entity-specific interfaces (UserRepository, ProjectRepository, etc.) extend
  the generic base and add domain-specific query methods (e.g. find_by_email).
- All methods use Optional and List from typing for explicitness.
- No storage detail leaks into this file — implementations live elsewhere.
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List

T = TypeVar("T")
ID = TypeVar("ID")


# ── Generic base interface ────────────────────────────────────────────────────

class Repository(ABC, Generic[T, ID]):
    """
    Generic repository interface defining standard CRUD operations.
    All entity-specific repositories extend this.
    """

    @abstractmethod
    def save(self, entity: T) -> None:
        """Create or update an entity in the store."""
        ...

    @abstractmethod
    def find_by_id(self, entity_id: ID) -> Optional[T]:
        """Return the entity with the given ID, or None if not found."""
        ...

    @abstractmethod
    def find_all(self) -> List[T]:
        """Return all stored entities."""
        ...

    @abstractmethod
    def delete(self, entity_id: ID) -> None:
        """Remove the entity with the given ID. No-op if not found."""
        ...

    @abstractmethod
    def exists(self, entity_id: ID) -> bool:
        """Return True if an entity with the given ID exists."""
        ...

    @abstractmethod
    def count(self) -> int:
        """Return the total number of stored entities."""
        ...


# ── Entity-specific interfaces ────────────────────────────────────────────────

class UserRepository(Repository):
    """
    Repository interface for User entities.
    Adds domain-specific queries on top of generic CRUD.
    """

    @abstractmethod
    def find_by_email(self, email: str):
        """Return the User with the given email, or None."""
        ...

    @abstractmethod
    def find_by_role(self, role) -> List:
        """Return all Users with the given UserRole."""
        ...

    @abstractmethod
    def find_by_status(self, status) -> List:
        """Return all Users with the given UserStatus."""
        ...


class ResearchProjectRepository(Repository):
    """
    Repository interface for ResearchProject entities.
    """

    @abstractmethod
    def find_by_owner(self, owner_id: str) -> List:
        """Return all projects owned by the given user ID."""
        ...

    @abstractmethod
    def find_by_status(self, status) -> List:
        """Return all projects with the given ProjectStatus."""
        ...

    @abstractmethod
    def find_by_member(self, user_id: str) -> List:
        """Return all projects where the user is a member."""
        ...


class DocumentRepository(Repository):
    """
    Repository interface for Document entities.
    """

    @abstractmethod
    def find_by_project(self, project_id: str) -> List:
        """Return all documents belonging to the given project."""
        ...

    @abstractmethod
    def find_by_status(self, status) -> List:
        """Return all documents with the given DocumentStatus."""
        ...

    @abstractmethod
    def find_by_uploader(self, user_id: str) -> List:
        """Return all documents uploaded by the given user."""
        ...


class TaskRepository(Repository):
    """
    Repository interface for Task entities.
    """

    @abstractmethod
    def find_by_project(self, project_id: str) -> List:
        """Return all tasks belonging to the given project."""
        ...

    @abstractmethod
    def find_by_assignee(self, user_id: str) -> List:
        """Return all tasks assigned to the given user."""
        ...

    @abstractmethod
    def find_by_status(self, status) -> List:
        """Return all tasks with the given TaskStatus."""
        ...

    @abstractmethod
    def find_overdue(self) -> List:
        """Return all tasks currently in OVERDUE status."""
        ...


class MessageRepository(Repository):
    """
    Repository interface for Message entities.
    """

    @abstractmethod
    def find_by_sender(self, sender_id: str) -> List:
        """Return all messages sent by the given user."""
        ...

    @abstractmethod
    def find_by_recipient(self, recipient_id: str) -> List:
        """Return all messages received by the given user."""
        ...

    @abstractmethod
    def find_unread(self, recipient_id: str) -> List:
        """Return all unread messages for the given recipient."""
        ...


class InvitationRepository(Repository):
    """
    Repository interface for Invitation entities.
    """

    @abstractmethod
    def find_by_project(self, project_id: str) -> List:
        """Return all invitations for the given project."""
        ...

    @abstractmethod
    def find_by_recipient(self, user_id: str) -> List:
        """Return all invitations sent to the given user."""
        ...

    @abstractmethod
    def find_pending(self, user_id: str) -> List:
        """Return all SENT (pending) invitations for the given user."""
        ...
