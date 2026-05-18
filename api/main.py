"""
api/main.py
FastAPI REST API for the University Research Collaboration Platform.

Exposes three entity APIs (minimum required by Assignment 12):
  /api/users      — User management
  /api/projects   — ResearchProject management
  /api/tasks      — Task management

Auto-generated Swagger UI available at: http://localhost:8000/docs
OpenAPI JSON available at:             http://localhost:8000/openapi.json

Run with:
  uvicorn api.main:app --reload
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date
from typing import List, Optional

from fastapi import FastAPI, HTTPException, status, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, field_validator

from factories.repository_factory import RepositoryFactory, STORAGE_MEMORY
from services.user_service import (
    UserService, UserNotFoundError, DuplicateEmailError,
    InvalidRoleError, UserNotActiveError,
)
from services.project_service import (
    ProjectService, ProjectNotFoundError, UnauthorizedError, ProjectStateError,
)
from services.task_service import (
    TaskService, TaskNotFoundError, TaskStateError,
    UnauthorizedError as TaskUnauthorizedError,
)

# ── App setup ─────────────────────────────────────────────────────────────────

app = FastAPI(
    title="University Research Collaboration Platform API",
    description=(
        "REST API for managing users, research projects, and tasks "
        "in the University Research Collaboration Platform. "
        "Built with FastAPI on top of the repository layer (Assignment 11)."
    ),
    version="1.0.0",
    contact={"name": "Platform Team"},
    license_info={"name": "MIT"},
)

# ── Repository and Service wiring (in-memory for now) ─────────────────────────

_user_repo = RepositoryFactory.get_user_repository(STORAGE_MEMORY)
_project_repo = RepositoryFactory.get_project_repository(STORAGE_MEMORY)
_task_repo = RepositoryFactory.get_task_repository(STORAGE_MEMORY)

user_service = UserService(_user_repo)
project_service = ProjectService(_project_repo, _user_repo)
task_service = TaskService(_task_repo, _user_repo, _project_repo)


# ════════════════════════════════════════════════════════════════════════════
# Pydantic schemas (request / response models)
# ════════════════════════════════════════════════════════════════════════════

# ── User schemas ──────────────────────────────────────────────────────────────

class UserCreateRequest(BaseModel):
    user_id: str
    name: str
    email: str
    password: str
    role: str

    model_config = {"json_schema_extra": {"example": {
        "user_id": "u-001",
        "name": "Alice Dube",
        "email": "alice@uni.ac.za",
        "password": "securepass",
        "role": "student",
    }}}


class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

    model_config = {"json_schema_extra": {"example": {
        "name": "Alice Updated",
        "email": "alice.new@uni.ac.za",
    }}}


class UserResponse(BaseModel):
    user_id: str
    name: str
    email: str
    role: str
    status: str
    created_date: str

    model_config = {"json_schema_extra": {"example": {
        "user_id": "u-001",
        "name": "Alice Dube",
        "email": "alice@uni.ac.za",
        "role": "STUDENT",
        "status": "ACTIVE",
        "created_date": "2026-01-15",
    }}}


def _user_to_response(user) -> UserResponse:
    return UserResponse(
        user_id=user.user_id,
        name=user.name,
        email=user.email,
        role=user.role.value,
        status=user.status.value,
        created_date=str(user.created_date),
    )


# ── Project schemas ───────────────────────────────────────────────────────────

class ProjectCreateRequest(BaseModel):
    project_id: str
    title: str
    description: str
    owner_id: str

    model_config = {"json_schema_extra": {"example": {
        "project_id": "proj-001",
        "title": "AI in Education Research",
        "description": "Exploring AI applications in South African universities.",
        "owner_id": "u-002",
    }}}


class AddMemberRequest(BaseModel):
    user_id: str
    requestor_id: str


class ProjectActionRequest(BaseModel):
    requestor_id: str


class ProjectResponse(BaseModel):
    project_id: str
    title: str
    description: str
    status: str
    owner_id: str
    owner_name: str
    member_count: int
    created_date: str

    model_config = {"json_schema_extra": {"example": {
        "project_id": "proj-001",
        "title": "AI in Education Research",
        "description": "Exploring AI applications.",
        "status": "ACTIVE",
        "owner_id": "u-002",
        "owner_name": "Prof Nkosi",
        "member_count": 3,
        "created_date": "2026-01-15",
    }}}


def _project_to_response(project) -> ProjectResponse:
    return ProjectResponse(
        project_id=project.project_id,
        title=project.title,
        description=project.description,
        status=project.status.value,
        owner_id=project.owner.user_id,
        owner_name=project.owner.name,
        member_count=len(project.get_members()),
        created_date=str(project.created_date),
    )


# ── Task schemas ──────────────────────────────────────────────────────────────

class TaskCreateRequest(BaseModel):
    task_id: str
    title: str
    description: str
    deadline: date
    project_id: str
    creator_id: str

    model_config = {"json_schema_extra": {"example": {
        "task_id": "task-001",
        "title": "Literature Review",
        "description": "Review 20 relevant academic papers.",
        "deadline": "2026-06-30",
        "project_id": "proj-001",
        "creator_id": "u-002",
    }}}


class AssignTaskRequest(BaseModel):
    assignee_id: str
    requestor_id: str


class TaskActionRequest(BaseModel):
    user_id: str


class TaskResponse(BaseModel):
    task_id: str
    title: str
    description: str
    deadline: str
    status: str
    assigned_to: Optional[str]
    created_by: str

    model_config = {"json_schema_extra": {"example": {
        "task_id": "task-001",
        "title": "Literature Review",
        "description": "Review 20 papers.",
        "deadline": "2026-06-30",
        "status": "ASSIGNED",
        "assigned_to": "u-001",
        "created_by": "u-002",
    }}}


def _task_to_response(task) -> TaskResponse:
    return TaskResponse(
        task_id=task.task_id,
        title=task.title,
        description=task.description,
        deadline=str(task.deadline),
        status=task.status.value,
        assigned_to=task.assigned_to.user_id if task.assigned_to else None,
        created_by=task.created_by.user_id,
    )


# ── Error response schema ─────────────────────────────────────────────────────

class ErrorResponse(BaseModel):
    detail: str


# ════════════════════════════════════════════════════════════════════════════
# USER ENDPOINTS  /api/users
# ════════════════════════════════════════════════════════════════════════════

@app.post(
    "/api/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    summary="Register a new user",
    responses={
        409: {"model": ErrorResponse, "description": "Email already in use"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
def register_user(request: UserCreateRequest):
    """
    Register a new user on the platform.

    - **user_id**: Unique identifier (you supply this).
    - **role**: One of `student`, `supervisor`, `researcher`, `admin`.
    - **password**: Minimum 6 characters.
    - **email**: Must be unique across all users.
    """
    try:
        user = user_service.register_user(
            request.user_id, request.name, request.email,
            request.password, request.role,
        )
        return _user_to_response(user)
    except DuplicateEmailError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except InvalidRoleError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.get(
    "/api/users",
    response_model=List[UserResponse],
    tags=["Users"],
    summary="Get all users",
)
def get_all_users(role: Optional[str] = Query(None, description="Filter by role")):
    """
    Return all users. Optionally filter by role using the `?role=` query parameter.
    """
    try:
        if role:
            users = user_service.get_users_by_role(role)
        else:
            users = user_service.get_all_users()
        return [_user_to_response(u) for u in users]
    except InvalidRoleError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.get(
    "/api/users/{user_id}",
    response_model=UserResponse,
    tags=["Users"],
    summary="Get a user by ID",
    responses={404: {"model": ErrorResponse, "description": "User not found"}},
)
def get_user(user_id: str):
    """Return a single user by their ID."""
    try:
        return _user_to_response(user_service.get_user(user_id))
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.put(
    "/api/users/{user_id}",
    response_model=UserResponse,
    tags=["Users"],
    summary="Update a user's profile",
    responses={
        404: {"model": ErrorResponse, "description": "User not found"},
        409: {"model": ErrorResponse, "description": "Email already in use"},
    },
)
def update_user(user_id: str, request: UserUpdateRequest):
    """Update a user's name and/or email address."""
    try:
        user = user_service.update_profile(user_id, request.name, request.email)
        return _user_to_response(user)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DuplicateEmailError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except (UserNotActiveError, ValueError) as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post(
    "/api/users/{user_id}/suspend",
    response_model=UserResponse,
    tags=["Users"],
    summary="Suspend a user account (admin action)",
    responses={404: {"model": ErrorResponse, "description": "User not found"}},
)
def suspend_user(user_id: str):
    """Suspend an active user account."""
    try:
        return _user_to_response(user_service.suspend_user(user_id))
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (UserNotActiveError, ValueError) as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post(
    "/api/users/{user_id}/reactivate",
    response_model=UserResponse,
    tags=["Users"],
    summary="Reactivate a suspended user (admin action)",
    responses={404: {"model": ErrorResponse, "description": "User not found"}},
)
def reactivate_user(user_id: str):
    """Reactivate a previously suspended user account."""
    try:
        return _user_to_response(user_service.reactivate_user(user_id))
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.delete(
    "/api/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Users"],
    summary="Deactivate (delete) a user account",
    responses={404: {"model": ErrorResponse, "description": "User not found"}},
)
def deactivate_user(user_id: str):
    """Deactivate a user account (soft delete)."""
    try:
        user_service.deactivate_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ════════════════════════════════════════════════════════════════════════════
# PROJECT ENDPOINTS  /api/projects
# ════════════════════════════════════════════════════════════════════════════

@app.post(
    "/api/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Projects"],
    summary="Create a new research project",
    responses={
        403: {"model": ErrorResponse, "description": "Unauthorized role"},
        404: {"model": ErrorResponse, "description": "Owner not found"},
    },
)
def create_project(request: ProjectCreateRequest):
    """
    Create a new research project.

    - **owner_id**: Must be an existing ACTIVE user with role `supervisor` or `researcher`.
    """
    try:
        project = project_service.create_project(
            request.project_id, request.title,
            request.description, request.owner_id,
        )
        return _project_to_response(project)
    except UnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=422, detail=str(e))


@app.get(
    "/api/projects",
    response_model=List[ProjectResponse],
    tags=["Projects"],
    summary="Get all projects",
)
def get_all_projects(
    owner_id: Optional[str] = Query(None, description="Filter by owner user ID"),
    member_id: Optional[str] = Query(None, description="Filter by member user ID"),
):
    """Return all projects. Filter by owner or member using query parameters."""
    if owner_id:
        projects = project_service.get_projects_by_owner(owner_id)
    elif member_id:
        projects = project_service.get_projects_by_member(member_id)
    else:
        projects = project_service.get_all_projects()
    return [_project_to_response(p) for p in projects]


@app.get(
    "/api/projects/{project_id}",
    response_model=ProjectResponse,
    tags=["Projects"],
    summary="Get a project by ID",
    responses={404: {"model": ErrorResponse, "description": "Project not found"}},
)
def get_project(project_id: str):
    """Return a single project by its ID."""
    try:
        return _project_to_response(project_service.get_project(project_id))
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post(
    "/api/projects/{project_id}/members",
    response_model=ProjectResponse,
    tags=["Projects"],
    summary="Add a member to a project",
    responses={
        403: {"model": ErrorResponse, "description": "Not the project owner"},
        404: {"model": ErrorResponse, "description": "Project or user not found"},
    },
)
def add_member(project_id: str, request: AddMemberRequest):
    """Add a user to a project. Only the project owner can do this."""
    try:
        project = project_service.add_member(
            project_id, request.user_id, request.requestor_id
        )
        return _project_to_response(project)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except (ProjectStateError, ValueError) as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post(
    "/api/projects/{project_id}/complete",
    response_model=ProjectResponse,
    tags=["Projects"],
    summary="Mark a project as completed",
    responses={
        403: {"model": ErrorResponse, "description": "Not the project owner"},
        404: {"model": ErrorResponse, "description": "Project not found"},
    },
)
def complete_project(project_id: str, request: ProjectActionRequest):
    """Mark an active project as completed. Only the owner can do this."""
    try:
        project = project_service.complete_project(project_id, request.requestor_id)
        return _project_to_response(project)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ProjectStateError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.delete(
    "/api/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Projects"],
    summary="Delete a project",
    responses={
        403: {"model": ErrorResponse, "description": "Not the project owner"},
        404: {"model": ErrorResponse, "description": "Project not found"},
    },
)
def delete_project(project_id: str, requestor_id: str = Query(...)):
    """Delete a project. Only the owner can delete; project must not be ACTIVE."""
    try:
        project_service.delete_project(project_id, requestor_id)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ProjectStateError as e:
        raise HTTPException(status_code=422, detail=str(e))


# ════════════════════════════════════════════════════════════════════════════
# TASK ENDPOINTS  /api/tasks
# ════════════════════════════════════════════════════════════════════════════

@app.post(
    "/api/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
    summary="Create a new task",
    responses={
        403: {"model": ErrorResponse, "description": "Unauthorized role"},
        404: {"model": ErrorResponse, "description": "User or project not found"},
    },
)
def create_task(request: TaskCreateRequest):
    """
    Create a task within a project.

    - **creator_id**: Must be SUPERVISOR or RESEARCHER.
    - **deadline**: Must be a future date.
    - **project_id**: Must be an existing ACTIVE project.
    """
    try:
        task = task_service.create_task(
            request.task_id, request.title, request.description,
            request.deadline, request.project_id, request.creator_id,
        )
        return _task_to_response(task)
    except TaskUnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except (TaskStateError, ValueError) as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=422, detail=str(e))


@app.get(
    "/api/tasks",
    response_model=List[TaskResponse],
    tags=["Tasks"],
    summary="Get all tasks",
)
def get_all_tasks(
    project_id: Optional[str] = Query(None, description="Filter by project ID"),
    assignee_id: Optional[str] = Query(None, description="Filter by assignee user ID"),
    overdue: Optional[bool] = Query(None, description="Return only overdue tasks"),
):
    """Return all tasks with optional filters."""
    if project_id:
        tasks = task_service.get_tasks_by_project(project_id)
    elif assignee_id:
        tasks = task_service.get_tasks_by_assignee(assignee_id)
    elif overdue:
        tasks = task_service.get_overdue_tasks()
    else:
        tasks = task_service.get_all_tasks()
    return [_task_to_response(t) for t in tasks]


@app.get(
    "/api/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["Tasks"],
    summary="Get a task by ID",
    responses={404: {"model": ErrorResponse, "description": "Task not found"}},
)
def get_task(task_id: str):
    """Return a single task by its ID."""
    try:
        return _task_to_response(task_service.get_task(task_id))
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post(
    "/api/tasks/{task_id}/assign",
    response_model=TaskResponse,
    tags=["Tasks"],
    summary="Assign a task to a student",
    responses={
        403: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Task or user not found"},
    },
)
def assign_task(task_id: str, request: AssignTaskRequest):
    """
    Assign a task to a user.

    - **requestor_id**: Must be SUPERVISOR or RESEARCHER.
    - **assignee_id**: The student to assign the task to.
    - Business rule: A student cannot have more than 10 active tasks at once.
    """
    try:
        task = task_service.assign_task(
            task_id, request.assignee_id, request.requestor_id
        )
        return _task_to_response(task)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TaskUnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except TaskStateError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=422, detail=str(e))


@app.post(
    "/api/tasks/{task_id}/start",
    response_model=TaskResponse,
    tags=["Tasks"],
    summary="Start working on a task",
    responses={
        403: {"model": ErrorResponse, "description": "Not the assigned user"},
        404: {"model": ErrorResponse, "description": "Task not found"},
    },
)
def start_task(task_id: str, request: TaskActionRequest):
    """Mark a task as IN_PROGRESS. Only the assigned user can do this."""
    try:
        return _task_to_response(task_service.start_task(task_id, request.user_id))
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TaskUnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except TaskStateError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post(
    "/api/tasks/{task_id}/complete",
    response_model=TaskResponse,
    tags=["Tasks"],
    summary="Mark a task as completed",
    responses={
        403: {"model": ErrorResponse, "description": "Not the assigned user"},
        404: {"model": ErrorResponse, "description": "Task not found"},
    },
)
def complete_task(task_id: str, request: TaskActionRequest):
    """Mark a task as COMPLETED. Only the assigned user can do this."""
    try:
        return _task_to_response(task_service.complete_task(task_id, request.user_id))
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TaskUnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except TaskStateError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.delete(
    "/api/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
    summary="Delete a task",
    responses={
        403: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Task not found"},
    },
)
def delete_task(task_id: str, requestor_id: str = Query(...)):
    """Delete a task. Only SUPERVISOR/RESEARCHER can delete non-active tasks."""
    try:
        task_service.delete_task(task_id, requestor_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TaskUnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except TaskStateError as e:
        raise HTTPException(status_code=422, detail=str(e))


# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/health", tags=["System"], summary="Health check")
def health():
    """Returns API status. Use this to verify the server is running."""
    return {"status": "ok", "version": "1.0.0"}
