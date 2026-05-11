"""
inmemory/implementations.py
In-memory HashMap-based repository implementations.

Each class:
  - Extends the matching entity-specific interface.
  - Stores entities in a plain Python dict (equivalent to a HashMap).
  - Implements all generic CRUD methods plus entity-specific queries.
  - Has no dependency on any storage technology — swapping to a database
    means replacing this file only; all service/business code is unchanged.
"""

from typing import Optional, List, Dict
from datetime import date

# Repository interfaces
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from repositories.interfaces import (
    UserRepository, ResearchProjectRepository,
    DocumentRepository, TaskRepository,
    MessageRepository, InvitationRepository,
)
from src.user import User, UserRole, UserStatus
from src.research_project import ResearchProject, ProjectStatus
from src.document import Document, DocumentStatus
from src.task import Task, TaskStatus
from src.communication import Message, MessageStatus, Invitation, InvitationStatus


# ── User ─────────────────────────────────────────────────────────────────────

class InMemoryUserRepository(UserRepository):
    """HashMap-backed User repository."""

    def __init__(self):
        self._storage: Dict[str, User] = {}

    # Generic CRUD
    def save(self, entity: User) -> None:
        self._storage[entity.user_id] = entity

    def find_by_id(self, entity_id: str) -> Optional[User]:
        return self._storage.get(entity_id)

    def find_all(self) -> List[User]:
        return list(self._storage.values())

    def delete(self, entity_id: str) -> None:
        self._storage.pop(entity_id, None)

    def exists(self, entity_id: str) -> bool:
        return entity_id in self._storage

    def count(self) -> int:
        return len(self._storage)

    # Domain-specific queries
    def find_by_email(self, email: str) -> Optional[User]:
        for user in self._storage.values():
            if user.email == email:
                return user
        return None

    def find_by_role(self, role: UserRole) -> List[User]:
        return [u for u in self._storage.values() if u.role == role]

    def find_by_status(self, status: UserStatus) -> List[User]:
        return [u for u in self._storage.values() if u.status == status]


# ── ResearchProject ───────────────────────────────────────────────────────────

class InMemoryResearchProjectRepository(ResearchProjectRepository):
    """HashMap-backed ResearchProject repository."""

    def __init__(self):
        self._storage: Dict[str, ResearchProject] = {}

    def save(self, entity: ResearchProject) -> None:
        self._storage[entity.project_id] = entity

    def find_by_id(self, entity_id: str) -> Optional[ResearchProject]:
        return self._storage.get(entity_id)

    def find_all(self) -> List[ResearchProject]:
        return list(self._storage.values())

    def delete(self, entity_id: str) -> None:
        self._storage.pop(entity_id, None)

    def exists(self, entity_id: str) -> bool:
        return entity_id in self._storage

    def count(self) -> int:
        return len(self._storage)

    def find_by_owner(self, owner_id: str) -> List[ResearchProject]:
        return [p for p in self._storage.values()
                if p.owner.user_id == owner_id]

    def find_by_status(self, status: ProjectStatus) -> List[ResearchProject]:
        return [p for p in self._storage.values() if p.status == status]

    def find_by_member(self, user_id: str) -> List[ResearchProject]:
        return [p for p in self._storage.values()
                if any(m.user_id == user_id for m in p.get_members())]


# ── Document ──────────────────────────────────────────────────────────────────

class InMemoryDocumentRepository(DocumentRepository):
    """
    HashMap-backed Document repository.
    Documents are stored with a composite key: project_id + document_id.
    """

    def __init__(self):
        self._storage: Dict[str, Document] = {}
        # Maps document_id → project_id for project-based queries
        self._project_index: Dict[str, str] = {}
        self._uploader_index: Dict[str, str] = {}

    def save(self, entity: Document) -> None:
        self._storage[entity.document_id] = entity

    def save_for_project(self, entity: Document, project_id: str,
                         uploader_id: str) -> None:
        """Save a document and record its project and uploader associations."""
        self._storage[entity.document_id] = entity
        self._project_index[entity.document_id] = project_id
        self._uploader_index[entity.document_id] = uploader_id

    def find_by_id(self, entity_id: str) -> Optional[Document]:
        return self._storage.get(entity_id)

    def find_all(self) -> List[Document]:
        return list(self._storage.values())

    def delete(self, entity_id: str) -> None:
        self._storage.pop(entity_id, None)
        self._project_index.pop(entity_id, None)
        self._uploader_index.pop(entity_id, None)

    def exists(self, entity_id: str) -> bool:
        return entity_id in self._storage

    def count(self) -> int:
        return len(self._storage)

    def find_by_project(self, project_id: str) -> List[Document]:
        matching_ids = [doc_id for doc_id, proj_id
                        in self._project_index.items()
                        if proj_id == project_id]
        return [self._storage[did] for did in matching_ids
                if did in self._storage]

    def find_by_status(self, status: DocumentStatus) -> List[Document]:
        return [d for d in self._storage.values() if d.status == status]

    def find_by_uploader(self, user_id: str) -> List[Document]:
        matching_ids = [doc_id for doc_id, uid
                        in self._uploader_index.items()
                        if uid == user_id]
        return [self._storage[did] for did in matching_ids
                if did in self._storage]


# ── Task ──────────────────────────────────────────────────────────────────────

class InMemoryTaskRepository(TaskRepository):
    """HashMap-backed Task repository."""

    def __init__(self):
        self._storage: Dict[str, Task] = {}
        self._project_index: Dict[str, str] = {}  # task_id → project_id

    def save(self, entity: Task) -> None:
        self._storage[entity.task_id] = entity

    def save_for_project(self, entity: Task, project_id: str) -> None:
        self._storage[entity.task_id] = entity
        self._project_index[entity.task_id] = project_id

    def find_by_id(self, entity_id: str) -> Optional[Task]:
        return self._storage.get(entity_id)

    def find_all(self) -> List[Task]:
        return list(self._storage.values())

    def delete(self, entity_id: str) -> None:
        self._storage.pop(entity_id, None)
        self._project_index.pop(entity_id, None)

    def exists(self, entity_id: str) -> bool:
        return entity_id in self._storage

    def count(self) -> int:
        return len(self._storage)

    def find_by_project(self, project_id: str) -> List[Task]:
        matching_ids = [tid for tid, pid in self._project_index.items()
                        if pid == project_id]
        return [self._storage[tid] for tid in matching_ids
                if tid in self._storage]

    def find_by_assignee(self, user_id: str) -> List[Task]:
        return [t for t in self._storage.values()
                if t.assigned_to and t.assigned_to.user_id == user_id]

    def find_by_status(self, status: TaskStatus) -> List[Task]:
        return [t for t in self._storage.values() if t.status == status]

    def find_overdue(self) -> List[Task]:
        return self.find_by_status(TaskStatus.OVERDUE)


# ── Message ───────────────────────────────────────────────────────────────────

class InMemoryMessageRepository(MessageRepository):
    """HashMap-backed Message repository."""

    def __init__(self):
        self._storage: Dict[str, Message] = {}

    def save(self, entity: Message) -> None:
        self._storage[entity.message_id] = entity

    def find_by_id(self, entity_id: str) -> Optional[Message]:
        return self._storage.get(entity_id)

    def find_all(self) -> List[Message]:
        return list(self._storage.values())

    def delete(self, entity_id: str) -> None:
        self._storage.pop(entity_id, None)

    def exists(self, entity_id: str) -> bool:
        return entity_id in self._storage

    def count(self) -> int:
        return len(self._storage)

    def find_by_sender(self, sender_id: str) -> List[Message]:
        return [m for m in self._storage.values()
                if m.sender.user_id == sender_id]

    def find_by_recipient(self, recipient_id: str) -> List[Message]:
        return [m for m in self._storage.values()
                if m.recipient.user_id == recipient_id]

    def find_unread(self, recipient_id: str) -> List[Message]:
        return [m for m in self.find_by_recipient(recipient_id)
                if m.status != MessageStatus.READ]


# ── Invitation ────────────────────────────────────────────────────────────────

class InMemoryInvitationRepository(InvitationRepository):
    """HashMap-backed Invitation repository."""

    def __init__(self):
        self._storage: Dict[str, Invitation] = {}

    def save(self, entity: Invitation) -> None:
        self._storage[entity.invitation_id] = entity

    def find_by_id(self, entity_id: str) -> Optional[Invitation]:
        return self._storage.get(entity_id)

    def find_all(self) -> List[Invitation]:
        return list(self._storage.values())

    def delete(self, entity_id: str) -> None:
        self._storage.pop(entity_id, None)

    def exists(self, entity_id: str) -> bool:
        return entity_id in self._storage

    def count(self) -> int:
        return len(self._storage)

    def find_by_project(self, project_id: str) -> List[Invitation]:
        return [i for i in self._storage.values()
                if i.project.project_id == project_id]

    def find_by_recipient(self, user_id: str) -> List[Invitation]:
        return [i for i in self._storage.values()
                if i.recipient.user_id == user_id]

    def find_pending(self, user_id: str) -> List[Invitation]:
        return [i for i in self.find_by_recipient(user_id)
                if i.status == InvitationStatus.SENT]
