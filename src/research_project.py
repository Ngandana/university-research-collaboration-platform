"""
research_project.py
ResearchProject entity for the University Research Collaboration Platform.
"""

from enum import Enum
from datetime import date
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from user import User


class ProjectStatus(Enum):
    CREATED = "CREATED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    ARCHIVED = "ARCHIVED"


class ResearchProject:
    """
    Represents a research project owned by a Supervisor.
    Contains Documents and Tasks (composition).
    Members join via accepted Invitations.
    """

    def __init__(self, project_id: str, title: str, description: str,
                 owner: "User"):
        self._project_id = project_id
        self._title = title
        self._description = description
        self._owner = owner
        self._status = ProjectStatus.CREATED
        self._created_date = date.today()
        self._end_date = None
        self._members: List["User"] = [owner]
        self._documents = []
        self._tasks = []

    # ── Getters ───────────────────────────────────────────────────────────────
    @property
    def project_id(self) -> str:
        return self._project_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def status(self) -> ProjectStatus:
        return self._status

    @property
    def owner(self) -> "User":
        return self._owner

    @property
    def created_date(self) -> date:
        return self._created_date

    @property
    def end_date(self):
        return self._end_date

    # ── Lifecycle methods ─────────────────────────────────────────────────────
    def activate(self) -> None:
        if self._status == ProjectStatus.CREATED:
            self._status = ProjectStatus.ACTIVE

    def complete(self) -> None:
        if self._status == ProjectStatus.ACTIVE:
            self._status = ProjectStatus.COMPLETED
            self._end_date = date.today()

    def cancel(self) -> None:
        if self._status in (ProjectStatus.CREATED, ProjectStatus.ACTIVE):
            self._status = ProjectStatus.CANCELLED
            self._end_date = date.today()

    def archive(self) -> None:
        if self._status in (ProjectStatus.COMPLETED, ProjectStatus.CANCELLED):
            self._status = ProjectStatus.ARCHIVED

    # ── Member management ─────────────────────────────────────────────────────
    def add_member(self, user: "User") -> None:
        if self._status == ProjectStatus.ARCHIVED:
            raise PermissionError("Cannot modify an archived project.")
        if user not in self._members:
            self._members.append(user)

    def remove_member(self, user: "User") -> None:
        if self._status == ProjectStatus.ARCHIVED:
            raise PermissionError("Cannot modify an archived project.")
        if user in self._members and user != self._owner:
            self._members.remove(user)

    def get_members(self) -> List["User"]:
        return list(self._members)

    def get_status(self) -> ProjectStatus:
        return self._status

    def __repr__(self) -> str:
        return (f"ResearchProject(id={self._project_id}, "
                f"title={self._title}, status={self._status.value})")
