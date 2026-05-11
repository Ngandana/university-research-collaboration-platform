"""
factories/repository_factory.py
Storage-Abstraction Mechanism — Factory Pattern.

A single RepositoryFactory.get_*_repository(storage_type) call returns the
correct repository implementation for the requested backend.

Why Factory (not pure DI) here:
  - The system must support runtime switching between storage backends
    (e.g. running tests with MEMORY, running production with DATABASE).
  - A factory centralises that decision in one place; adding a new backend
    only requires adding one new case here and one new implementation file.
  - Pure DI would be wired at app startup and would not support dynamic
    switching without a DI container (overkill for this scope).

Supported storage types (string constants):
  "MEMORY"      — InMemory HashMap (Assignment 10 / 11)
  "FILESYSTEM"  — JSON file-based (stub, future sprint)
  "DATABASE"    — PostgreSQL via psycopg2 (stub, future sprint)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from repositories.interfaces import (
    UserRepository, ResearchProjectRepository,
    DocumentRepository, TaskRepository,
    MessageRepository, InvitationRepository,
)
from repositories.inmemory.implementations import (
    InMemoryUserRepository,
    InMemoryResearchProjectRepository,
    InMemoryDocumentRepository,
    InMemoryTaskRepository,
    InMemoryMessageRepository,
    InMemoryInvitationRepository,
)
from repositories.stubs import (
    FileSystemUserRepository,
    FileSystemResearchProjectRepository,
    DatabaseUserRepository,
    DatabaseResearchProjectRepository,
)

# Valid storage type constants
STORAGE_MEMORY = "MEMORY"
STORAGE_FILESYSTEM = "FILESYSTEM"
STORAGE_DATABASE = "DATABASE"

_VALID_TYPES = {STORAGE_MEMORY, STORAGE_FILESYSTEM, STORAGE_DATABASE}


def _validate(storage_type: str) -> str:
    t = storage_type.upper().strip()
    if t not in _VALID_TYPES:
        raise ValueError(
            f"Unknown storage type '{storage_type}'. "
            f"Valid options: {sorted(_VALID_TYPES)}"
        )
    return t


class RepositoryFactory:
    """
    Central factory that returns the correct repository implementation
    based on the requested storage backend.

    Usage:
        repo = RepositoryFactory.get_user_repository("MEMORY")
        repo.save(user)
    """

    @staticmethod
    def get_user_repository(storage_type: str = STORAGE_MEMORY) -> UserRepository:
        t = _validate(storage_type)
        if t == STORAGE_MEMORY:
            return InMemoryUserRepository()
        if t == STORAGE_FILESYSTEM:
            return FileSystemUserRepository()
        if t == STORAGE_DATABASE:
            return DatabaseUserRepository()

    @staticmethod
    def get_project_repository(storage_type: str = STORAGE_MEMORY) -> ResearchProjectRepository:
        t = _validate(storage_type)
        if t == STORAGE_MEMORY:
            return InMemoryResearchProjectRepository()
        if t == STORAGE_FILESYSTEM:
            return FileSystemResearchProjectRepository()
        if t == STORAGE_DATABASE:
            return DatabaseResearchProjectRepository()

    @staticmethod
    def get_document_repository(storage_type: str = STORAGE_MEMORY) -> DocumentRepository:
        t = _validate(storage_type)
        if t == STORAGE_MEMORY:
            return InMemoryDocumentRepository()
        raise NotImplementedError(
            f"DocumentRepository not yet implemented for '{t}'. "
            "Add a stub in repositories/stubs.py."
        )

    @staticmethod
    def get_task_repository(storage_type: str = STORAGE_MEMORY) -> TaskRepository:
        t = _validate(storage_type)
        if t == STORAGE_MEMORY:
            return InMemoryTaskRepository()
        raise NotImplementedError(
            f"TaskRepository not yet implemented for '{t}'."
        )

    @staticmethod
    def get_message_repository(storage_type: str = STORAGE_MEMORY) -> MessageRepository:
        t = _validate(storage_type)
        if t == STORAGE_MEMORY:
            return InMemoryMessageRepository()
        raise NotImplementedError(
            f"MessageRepository not yet implemented for '{t}'."
        )

    @staticmethod
    def get_invitation_repository(storage_type: str = STORAGE_MEMORY) -> InvitationRepository:
        t = _validate(storage_type)
        if t == STORAGE_MEMORY:
            return InMemoryInvitationRepository()
        raise NotImplementedError(
            f"InvitationRepository not yet implemented for '{t}'."
        )
