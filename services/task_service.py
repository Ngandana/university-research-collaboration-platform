"""
services/task_service.py
Service layer for Task business operations.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from typing import List
from datetime import date
from src.task import Task, TaskStatus
from src.user import UserRole, UserStatus
from src.research_project import ProjectStatus
from repositories.interfaces import TaskRepository, UserRepository, ResearchProjectRepository


# ── Custom exceptions ─────────────────────────────────────────────────────────

class TaskNotFoundError(Exception):
    def __init__(self, task_id: str):
        super().__init__(f"Task '{task_id}' not found.")
        self.task_id = task_id


class TaskStateError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class UnauthorizedError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


# ── Service ───────────────────────────────────────────────────────────────────

class TaskService:
    """
    Encapsulates all business logic relating to Task management.
    """

    MAX_ACTIVE_TASKS_PER_STUDENT = 10

    def __init__(self, task_repository: TaskRepository,
                 user_repository: UserRepository,
                 project_repository: ResearchProjectRepository):
        self._task_repo = task_repository
        self._user_repo = user_repository
        self._project_repo = project_repository

    # ── Create ────────────────────────────────────────────────────────────────

    def create_task(self, task_id: str, title: str, description: str,
                    deadline: date, project_id: str,
                    creator_id: str) -> Task:
        """
        Create a new task within a project.
        Business rules:
          - Creator must be SUPERVISOR or RESEARCHER and be ACTIVE.
          - Project must be ACTIVE.
          - Deadline must be in the future.
          - Title cannot be empty.
          - Task ID must be unique.
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty.")

        if deadline <= date.today():
            raise ValueError("Task deadline must be in the future.")

        if self._task_repo.exists(task_id):
            raise ValueError(f"Task ID '{task_id}' is already in use.")

        creator = self._user_repo.find_by_id(creator_id)
        if not creator:
            from services.user_service import UserNotFoundError
            raise UserNotFoundError(creator_id)

        if creator.status != UserStatus.ACTIVE:
            raise UnauthorizedError(
                f"User '{creator_id}' must be active to create tasks."
            )

        if creator.role not in (UserRole.SUPERVISOR, UserRole.RESEARCHER):
            raise UnauthorizedError(
                "Only Supervisors and Researchers can create tasks."
            )

        project = self._project_repo.find_by_id(project_id)
        if not project:
            from services.project_service import ProjectNotFoundError
            raise ProjectNotFoundError(project_id)

        if project.status != ProjectStatus.ACTIVE:
            raise TaskStateError(
                f"Cannot add tasks to a project with status "
                f"'{project.status.value}'."
            )

        task = Task(task_id, title, description, deadline, creator)
        self._task_repo.save_for_project(task, project_id)
        return task

    # ── Read ──────────────────────────────────────────────────────────────────

    def get_task(self, task_id: str) -> Task:
        task = self._task_repo.find_by_id(task_id)
        if not task:
            raise TaskNotFoundError(task_id)
        return task

    def get_all_tasks(self) -> List[Task]:
        return self._task_repo.find_all()

    def get_tasks_by_project(self, project_id: str) -> List[Task]:
        return self._task_repo.find_by_project(project_id)

    def get_tasks_by_assignee(self, user_id: str) -> List[Task]:
        return self._task_repo.find_by_assignee(user_id)

    def get_overdue_tasks(self) -> List[Task]:
        return self._task_repo.find_overdue()

    # ── Update — Assign ───────────────────────────────────────────────────────

    def assign_task(self, task_id: str, assignee_id: str,
                    requestor_id: str) -> Task:
        """
        Assign a task to a student.
        Business rules:
          - Only SUPERVISOR or RESEARCHER can assign tasks.
          - Assignee must be ACTIVE.
          - Assignee cannot have more than MAX_ACTIVE_TASKS_PER_STUDENT
            tasks in ASSIGNED or IN_PROGRESS status simultaneously.
          - Task must be in CREATED or ASSIGNED status.
        """
        task = self.get_task(task_id)

        requestor = self._user_repo.find_by_id(requestor_id)
        if not requestor or requestor.role not in (UserRole.SUPERVISOR,
                                                    UserRole.RESEARCHER):
            raise UnauthorizedError("Only Supervisors and Researchers can assign tasks.")

        assignee = self._user_repo.find_by_id(assignee_id)
        if not assignee:
            from services.user_service import UserNotFoundError
            raise UserNotFoundError(assignee_id)

        if assignee.status != UserStatus.ACTIVE:
            raise UnauthorizedError(
                f"Cannot assign tasks to user '{assignee_id}' — not active."
            )

        if task.status not in (TaskStatus.CREATED, TaskStatus.ASSIGNED):
            raise TaskStateError(
                f"Task '{task_id}' cannot be assigned in its current "
                f"status '{task.status.value}'."
            )

        # Enforce active task limit
        active_tasks = [
            t for t in self._task_repo.find_by_assignee(assignee_id)
            if t.status in (TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS)
        ]
        if len(active_tasks) >= self.MAX_ACTIVE_TASKS_PER_STUDENT:
            raise TaskStateError(
                f"User '{assignee_id}' already has "
                f"{self.MAX_ACTIVE_TASKS_PER_STUDENT} active tasks. "
                "Complete some before assigning more."
            )

        task.assign(assignee)
        self._task_repo.save(task)
        return task

    # ── Update — Progress ─────────────────────────────────────────────────────

    def start_task(self, task_id: str, user_id: str) -> Task:
        """
        Mark a task as IN_PROGRESS.
        Business rule: Only the assigned student can start the task.
        """
        task = self.get_task(task_id)

        if not task.assigned_to or task.assigned_to.user_id != user_id:
            raise UnauthorizedError(
                f"Only the assigned user can start task '{task_id}'."
            )

        if task.status != TaskStatus.ASSIGNED:
            raise TaskStateError(
                f"Task '{task_id}' must be ASSIGNED before it can be started. "
                f"Current status: '{task.status.value}'."
            )

        task.start()
        self._task_repo.save(task)
        return task

    def complete_task(self, task_id: str, user_id: str) -> Task:
        """
        Mark a task as COMPLETED.
        Business rule: Only the assigned student can complete the task.
        """
        task = self.get_task(task_id)

        if not task.assigned_to or task.assigned_to.user_id != user_id:
            raise UnauthorizedError(
                f"Only the assigned user can complete task '{task_id}'."
            )

        if task.status not in (TaskStatus.IN_PROGRESS, TaskStatus.OVERDUE):
            raise TaskStateError(
                f"Task must be IN_PROGRESS or OVERDUE to be completed. "
                f"Current status: '{task.status.value}'."
            )

        task.complete()
        self._task_repo.save(task)
        return task

    # ── Delete ────────────────────────────────────────────────────────────────

    def delete_task(self, task_id: str, requestor_id: str) -> None:
        """
        Delete a task.
        Business rule: Only SUPERVISOR/RESEARCHER can delete tasks;
        task must not be IN_PROGRESS or COMPLETED.
        """
        task = self.get_task(task_id)

        requestor = self._user_repo.find_by_id(requestor_id)
        if not requestor or requestor.role not in (UserRole.SUPERVISOR,
                                                    UserRole.RESEARCHER):
            raise UnauthorizedError("Only Supervisors and Researchers can delete tasks.")

        if task.status in (TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED):
            raise TaskStateError(
                f"Cannot delete a task that is '{task.status.value}'."
            )

        self._task_repo.delete(task_id)
