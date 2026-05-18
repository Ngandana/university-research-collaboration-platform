"""
services/project_service.py
Service layer for ResearchProject business operations.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from typing import List
from src.research_project import ResearchProject, ProjectStatus
from src.user import UserRole, UserStatus
from repositories.interfaces import ResearchProjectRepository, UserRepository


# ── Custom exceptions ─────────────────────────────────────────────────────────

class ProjectNotFoundError(Exception):
    def __init__(self, project_id: str):
        super().__init__(f"Project '{project_id}' not found.")
        self.project_id = project_id


class UnauthorizedError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ProjectStateError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


# ── Service ───────────────────────────────────────────────────────────────────

class ProjectService:
    """
    Encapsulates all business logic relating to ResearchProject management.
    Injected with both a project repository and a user repository so it can
    validate owner existence and role without depending on UserService directly.
    """

    def __init__(self, project_repository: ResearchProjectRepository,
                 user_repository: UserRepository):
        self._project_repo = project_repository
        self._user_repo = user_repository

    # ── Create ────────────────────────────────────────────────────────────────

    def create_project(self, project_id: str, title: str,
                       description: str, owner_id: str) -> ResearchProject:
        """
        Create a new research project.
        Business rules:
          - Owner must exist and be ACTIVE.
          - Owner must have role SUPERVISOR or RESEARCHER.
          - Title cannot be empty.
          - Project ID must be unique.
        """
        if not title or not title.strip():
            raise ValueError("Project title cannot be empty.")

        if self._project_repo.exists(project_id):
            raise ValueError(f"Project ID '{project_id}' is already in use.")

        owner = self._user_repo.find_by_id(owner_id)
        if not owner:
            from services.user_service import UserNotFoundError
            raise UserNotFoundError(owner_id)

        if owner.status != UserStatus.ACTIVE:
            raise UnauthorizedError(
                f"User '{owner_id}' must be active to create a project."
            )

        if owner.role not in (UserRole.SUPERVISOR, UserRole.RESEARCHER):
            raise UnauthorizedError(
                f"Only Supervisors and Researchers can create projects. "
                f"User '{owner_id}' has role '{owner.role.value}'."
            )

        project = ResearchProject(project_id, title, description, owner)
        project.activate()
        self._project_repo.save(project)
        return project

    # ── Read ──────────────────────────────────────────────────────────────────

    def get_project(self, project_id: str) -> ResearchProject:
        """Return a project by ID or raise ProjectNotFoundError."""
        project = self._project_repo.find_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(project_id)
        return project

    def get_all_projects(self) -> List[ResearchProject]:
        return self._project_repo.find_all()

    def get_projects_by_owner(self, owner_id: str) -> List[ResearchProject]:
        return self._project_repo.find_by_owner(owner_id)

    def get_projects_by_member(self, user_id: str) -> List[ResearchProject]:
        return self._project_repo.find_by_member(user_id)

    # ── Update ────────────────────────────────────────────────────────────────

    def add_member(self, project_id: str, user_id: str,
                   requestor_id: str) -> ResearchProject:
        """
        Add a member to a project.
        Business rules:
          - Only the project owner can add members.
          - Project must be ACTIVE.
          - User to add must exist and be ACTIVE.
        """
        project = self.get_project(project_id)

        if project.owner.user_id != requestor_id:
            raise UnauthorizedError(
                f"Only the project owner can add members."
            )

        if project.status != ProjectStatus.ACTIVE:
            raise ProjectStateError(
                f"Cannot add members to a project with status "
                f"'{project.status.value}'."
            )

        user = self._user_repo.find_by_id(user_id)
        if not user:
            from services.user_service import UserNotFoundError
            raise UserNotFoundError(user_id)

        if user.status != UserStatus.ACTIVE:
            raise UnauthorizedError(
                f"User '{user_id}' must be active to join a project."
            )

        project.add_member(user)
        self._project_repo.save(project)
        return project

    def complete_project(self, project_id: str,
                         requestor_id: str) -> ResearchProject:
        """
        Mark a project as completed.
        Business rule: Only the owner can complete their project.
        """
        project = self.get_project(project_id)

        if project.owner.user_id != requestor_id:
            raise UnauthorizedError("Only the project owner can complete the project.")

        if project.status != ProjectStatus.ACTIVE:
            raise ProjectStateError(
                f"Only ACTIVE projects can be completed. "
                f"Current status: '{project.status.value}'."
            )

        project.complete()
        self._project_repo.save(project)
        return project

    def archive_project(self, project_id: str) -> ResearchProject:
        """Archive a completed or cancelled project."""
        project = self.get_project(project_id)

        if project.status not in (ProjectStatus.COMPLETED, ProjectStatus.CANCELLED):
            raise ProjectStateError(
                "Only COMPLETED or CANCELLED projects can be archived."
            )

        project.archive()
        self._project_repo.save(project)
        return project

    # ── Delete ────────────────────────────────────────────────────────────────

    def delete_project(self, project_id: str,
                       requestor_id: str) -> None:
        """
        Delete a project record entirely.
        Business rule: Only the owner can delete; project must not be ACTIVE.
        """
        project = self.get_project(project_id)

        if project.owner.user_id != requestor_id:
            raise UnauthorizedError("Only the project owner can delete the project.")

        if project.status == ProjectStatus.ACTIVE:
            raise ProjectStateError(
                "Cannot delete an ACTIVE project. Complete or cancel it first."
            )

        self._project_repo.delete(project_id)
