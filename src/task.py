"""
task.py
Task entity for the University Research Collaboration Platform.
"""

from enum import Enum
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from user import User


class TaskStatus(Enum):
    CREATED = "CREATED"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    OVERDUE = "OVERDUE"


class Task:
    """
    Represents a research task within a project.
    Created and assigned by a Supervisor; completed by a Student.
    Business rules:
      - A task is automatically OVERDUE if its deadline passes without completion.
    """

    def __init__(self, task_id: str, title: str, description: str,
                 deadline: date, created_by: "User"):
        self._task_id = task_id
        self._title = title
        self._description = description
        self._deadline = deadline
        self._created_by = created_by
        self._assigned_to: "User" = None
        self._status = TaskStatus.CREATED

    # ── Getters ───────────────────────────────────────────────────────────────
    @property
    def task_id(self) -> str:
        return self._task_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def deadline(self) -> date:
        return self._deadline

    @property
    def status(self) -> TaskStatus:
        return self._status

    @property
    def assigned_to(self) -> "User":
        return self._assigned_to

    @property
    def created_by(self) -> "User":
        return self._created_by

    # ── Lifecycle methods ─────────────────────────────────────────────────────
    def assign(self, user: "User") -> None:
        """Supervisor assigns the task to a user."""
        if self._status not in (TaskStatus.CREATED, TaskStatus.ASSIGNED):
            raise ValueError("Only CREATED or ASSIGNED tasks can be reassigned.")
        self._assigned_to = user
        self._status = TaskStatus.ASSIGNED

    def start(self) -> None:
        """Student begins working on the task."""
        if self._status == TaskStatus.ASSIGNED:
            self._status = TaskStatus.IN_PROGRESS

    def complete(self) -> None:
        """Mark the task as completed."""
        if self._status in (TaskStatus.IN_PROGRESS, TaskStatus.OVERDUE):
            self._status = TaskStatus.COMPLETED

    def mark_overdue(self) -> None:
        """System marks task overdue if deadline has passed."""
        if (self._status in (TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS)
                and date.today() > self._deadline):
            self._status = TaskStatus.OVERDUE

    def update_status(self, status: TaskStatus) -> None:
        """Direct status update (admin use)."""
        self._status = status

    def get_status(self) -> TaskStatus:
        return self._status

    def __repr__(self) -> str:
        return (f"Task(id={self._task_id}, title={self._title}, "
                f"status={self._status.value}, deadline={self._deadline})")
