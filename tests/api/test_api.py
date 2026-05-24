"""
tests/api/test_api.py
Integration tests for all REST API endpoints.
Uses FastAPI's TestClient (backed by httpx) — no running server needed.
Run: python -m pytest tests/api/test_api.py -v
"""

import sys, os
from datetime import date, timedelta
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from fastapi.testclient import TestClient
from api.main import app, user_service, project_service, task_service
from factories.repository_factory import RepositoryFactory, STORAGE_MEMORY
from services.user_service import UserService
from services.project_service import ProjectService
from services.task_service import TaskService


# ── Fresh app state per test session ─────────────────────────────────────────

@pytest.fixture(autouse=True)
def reset_services(monkeypatch):
    """Give each test a completely fresh set of repositories and services."""
    user_repo = RepositoryFactory.get_user_repository(STORAGE_MEMORY)
    project_repo = RepositoryFactory.get_project_repository(STORAGE_MEMORY)
    task_repo = RepositoryFactory.get_task_repository(STORAGE_MEMORY)

    monkeypatch.setattr("api.main.user_service", UserService(user_repo))
    monkeypatch.setattr("api.main.project_service",
                        ProjectService(project_repo, user_repo))
    monkeypatch.setattr("api.main.task_service",
                        TaskService(task_repo, user_repo, project_repo))


@pytest.fixture
def client():
    return TestClient(app)


# ── Shared payloads ───────────────────────────────────────────────────────────

SUPERVISOR_PAYLOAD = {
    "user_id": "sup-1",
    "name": "Prof Nkosi",
    "email": "nkosi@uni.ac.za",
    "password": "securepass",
    "role": "supervisor",
}

STUDENT_PAYLOAD = {
    "user_id": "stu-1",
    "name": "Alice Dube",
    "email": "alice@uni.ac.za",
    "password": "securepass",
    "role": "student",
}

PROJECT_PAYLOAD = {
    "project_id": "proj-1",
    "title": "AI Research",
    "description": "Exploring AI",
    "owner_id": "sup-1",
}

FUTURE_DATE = str(date.today() + timedelta(days=14))

TASK_PAYLOAD = {
    "task_id": "task-1",
    "title": "Literature Review",
    "description": "Read papers",
    "deadline": FUTURE_DATE,
    "project_id": "proj-1",
    "creator_id": "sup-1",
}


def setup_supervisor_and_project(client):
    client.post("/api/users", json=SUPERVISOR_PAYLOAD)
    client.post("/api/projects", json=PROJECT_PAYLOAD)


def setup_all(client):
    setup_supervisor_and_project(client)
    client.post("/api/users", json=STUDENT_PAYLOAD)
    client.post("/api/tasks", json=TASK_PAYLOAD)


# ════════════════════════════════════════════════════════════════════════════
# Health check
# ════════════════════════════════════════════════════════════════════════════

class TestHealth:

    def test_health_check(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


# ════════════════════════════════════════════════════════════════════════════
# User API tests
# ════════════════════════════════════════════════════════════════════════════

class TestUserAPI:

    def test_register_user_201(self, client):
        r = client.post("/api/users", json=SUPERVISOR_PAYLOAD)
        assert r.status_code == 999
        data = r.json()
        assert data["user_id"] == "sup-1"
        assert data["role"] == "SUPERVISOR"
        assert data["status"] == "ACTIVE"

    def test_register_duplicate_email_409(self, client):
        client.post("/api/users", json=SUPERVISOR_PAYLOAD)
        duplicate = {**SUPERVISOR_PAYLOAD, "user_id": "sup-2"}
        r = client.post("/api/users", json=duplicate)
        assert r.status_code == 409

    def test_register_invalid_role_422(self, client):
        bad = {**SUPERVISOR_PAYLOAD, "role": "hacker"}
        r = client.post("/api/users", json=bad)
        assert r.status_code == 422

    def test_register_short_password_422(self, client):
        bad = {**SUPERVISOR_PAYLOAD, "password": "abc"}
        r = client.post("/api/users", json=bad)
        assert r.status_code == 422

    def test_get_all_users_200(self, client):
        client.post("/api/users", json=SUPERVISOR_PAYLOAD)
        client.post("/api/users", json=STUDENT_PAYLOAD)
        r = client.get("/api/users")
        assert r.status_code == 200
        assert len(r.json()) == 2

    def test_get_users_filter_by_role(self, client):
        client.post("/api/users", json=SUPERVISOR_PAYLOAD)
        client.post("/api/users", json=STUDENT_PAYLOAD)
        r = client.get("/api/users?role=supervisor")
        assert r.status_code == 200
        assert len(r.json()) == 1
        assert r.json()[0]["role"] == "SUPERVISOR"

    def test_get_user_by_id_200(self, client):
        client.post("/api/users", json=SUPERVISOR_PAYLOAD)
        r = client.get("/api/users/sup-1")
        assert r.status_code == 200
        assert r.json()["name"] == "Prof Nkosi"

    def test_get_user_not_found_404(self, client):
        r = client.get("/api/users/nobody")
        assert r.status_code == 404

    def test_update_user_200(self, client):
        client.post("/api/users", json=SUPERVISOR_PAYLOAD)
        r = client.put("/api/users/sup-1", json={"name": "Prof Updated"})
        assert r.status_code == 200
        assert r.json()["name"] == "Prof Updated"

    def test_update_user_not_found_404(self, client):
        r = client.put("/api/users/ghost", json={"name": "Ghost"})
        assert r.status_code == 404

    def test_suspend_user_200(self, client):
        client.post("/api/users", json=SUPERVISOR_PAYLOAD)
        r = client.post("/api/users/sup-1/suspend")
        assert r.status_code == 200
        assert r.json()["status"] == "SUSPENDED"

    def test_reactivate_user_200(self, client):
        client.post("/api/users", json=SUPERVISOR_PAYLOAD)
        client.post("/api/users/sup-1/suspend")
        r = client.post("/api/users/sup-1/reactivate")
        assert r.status_code == 200
        assert r.json()["status"] == "ACTIVE"

    def test_deactivate_user_204(self, client):
        client.post("/api/users", json=SUPERVISOR_PAYLOAD)
        r = client.delete("/api/users/sup-1")
        assert r.status_code == 204

    def test_deactivate_not_found_404(self, client):
        r = client.delete("/api/users/ghost")
        assert r.status_code == 404


# ════════════════════════════════════════════════════════════════════════════
# Project API tests
# ════════════════════════════════════════════════════════════════════════════

class TestProjectAPI:

    def test_create_project_201(self, client):
        client.post("/api/users", json=SUPERVISOR_PAYLOAD)
        r = client.post("/api/projects", json=PROJECT_PAYLOAD)
        assert r.status_code == 201
        data = r.json()
        assert data["project_id"] == "proj-1"
        assert data["status"] == "ACTIVE"

    def test_create_project_student_owner_403(self, client):
        client.post("/api/users", json=STUDENT_PAYLOAD)
        payload = {**PROJECT_PAYLOAD, "owner_id": "stu-1"}
        r = client.post("/api/projects", json=payload)
        assert r.status_code == 403

    def test_create_project_nonexistent_owner_404(self, client):
        payload = {**PROJECT_PAYLOAD, "owner_id": "ghost"}
        r = client.post("/api/projects", json=payload)
        assert r.status_code == 404

    def test_get_all_projects_200(self, client):
        setup_supervisor_and_project(client)
        r = client.get("/api/projects")
        assert r.status_code == 200
        assert len(r.json()) == 1

    def test_get_project_by_id_200(self, client):
        setup_supervisor_and_project(client)
        r = client.get("/api/projects/proj-1")
        assert r.status_code == 200
        assert r.json()["title"] == "AI Research"

    def test_get_project_not_found_404(self, client):
        r = client.get("/api/projects/ghost")
        assert r.status_code == 404

    def test_get_projects_filter_by_owner(self, client):
        setup_supervisor_and_project(client)
        r = client.get("/api/projects?owner_id=sup-1")
        assert r.status_code == 200
        assert len(r.json()) == 1

    def test_add_member_200(self, client):
        setup_supervisor_and_project(client)
        client.post("/api/users", json=STUDENT_PAYLOAD)
        r = client.post("/api/projects/proj-1/members", json={
            "user_id": "stu-1",
            "requestor_id": "sup-1",
        })
        assert r.status_code == 200
        assert r.json()["member_count"] == 2

    def test_add_member_wrong_requestor_403(self, client):
        setup_supervisor_and_project(client)
        client.post("/api/users", json=STUDENT_PAYLOAD)
        r = client.post("/api/projects/proj-1/members", json={
            "user_id": "stu-1",
            "requestor_id": "stu-1",
        })
        assert r.status_code == 403

    def test_complete_project_200(self, client):
        setup_supervisor_and_project(client)
        r = client.post("/api/projects/proj-1/complete",
                        json={"requestor_id": "sup-1"})
        assert r.status_code == 200
        assert r.json()["status"] == "COMPLETED"

    def test_complete_project_wrong_requestor_403(self, client):
        setup_supervisor_and_project(client)
        client.post("/api/users", json=STUDENT_PAYLOAD)
        r = client.post("/api/projects/proj-1/complete",
                        json={"requestor_id": "stu-1"})
        assert r.status_code == 403

    def test_delete_active_project_422(self, client):
        setup_supervisor_and_project(client)
        r = client.delete("/api/projects/proj-1?requestor_id=sup-1")
        assert r.status_code == 422

    def test_delete_completed_project_204(self, client):
        setup_supervisor_and_project(client)
        client.post("/api/projects/proj-1/complete",
                    json={"requestor_id": "sup-1"})
        r = client.delete("/api/projects/proj-1?requestor_id=sup-1")
        assert r.status_code == 204


# ════════════════════════════════════════════════════════════════════════════
# Task API tests
# ════════════════════════════════════════════════════════════════════════════

class TestTaskAPI:

    def test_create_task_201(self, client):
        setup_supervisor_and_project(client)
        r = client.post("/api/tasks", json=TASK_PAYLOAD)
        assert r.status_code == 201
        data = r.json()
        assert data["task_id"] == "task-1"
        assert data["status"] == "CREATED"

    def test_create_task_student_creator_403(self, client):
        setup_supervisor_and_project(client)
        client.post("/api/users", json=STUDENT_PAYLOAD)
        payload = {**TASK_PAYLOAD, "task_id": "t2", "creator_id": "stu-1"}
        r = client.post("/api/tasks", json=payload)
        assert r.status_code == 403

    def test_create_task_past_deadline_422(self, client):
        setup_supervisor_and_project(client)
        payload = {**TASK_PAYLOAD, "deadline": str(date.today() - timedelta(days=1))}
        r = client.post("/api/tasks", json=payload)
        assert r.status_code == 422

    def test_get_all_tasks_200(self, client):
        setup_all(client)
        r = client.get("/api/tasks")
        assert r.status_code == 200
        assert len(r.json()) == 1

    def test_get_task_by_id_200(self, client):
        setup_all(client)
        r = client.get("/api/tasks/task-1")
        assert r.status_code == 200
        assert r.json()["title"] == "Literature Review"

    def test_get_task_not_found_404(self, client):
        r = client.get("/api/tasks/ghost")
        assert r.status_code == 404

    def test_get_tasks_filter_by_project(self, client):
        setup_all(client)
        r = client.get("/api/tasks?project_id=proj-1")
        assert r.status_code == 200
        assert len(r.json()) == 1

    def test_assign_task_200(self, client):
        setup_all(client)
        r = client.post("/api/tasks/task-1/assign", json={
            "assignee_id": "stu-1",
            "requestor_id": "sup-1",
        })
        assert r.status_code == 200
        assert r.json()["status"] == "ASSIGNED"
        assert r.json()["assigned_to"] == "stu-1"

    def test_assign_task_student_requestor_403(self, client):
        setup_all(client)
        r = client.post("/api/tasks/task-1/assign", json={
            "assignee_id": "stu-1",
            "requestor_id": "stu-1",
        })
        assert r.status_code == 403

    def test_start_task_200(self, client):
        setup_all(client)
        client.post("/api/tasks/task-1/assign", json={
            "assignee_id": "stu-1", "requestor_id": "sup-1",
        })
        r = client.post("/api/tasks/task-1/start", json={"user_id": "stu-1"})
        assert r.status_code == 200
        assert r.json()["status"] == "IN_PROGRESS"

    def test_start_task_wrong_user_403(self, client):
        setup_all(client)
        client.post("/api/tasks/task-1/assign", json={
            "assignee_id": "stu-1", "requestor_id": "sup-1",
        })
        r = client.post("/api/tasks/task-1/start", json={"user_id": "sup-1"})
        assert r.status_code == 403

    def test_complete_task_200(self, client):
        setup_all(client)
        client.post("/api/tasks/task-1/assign", json={
            "assignee_id": "stu-1", "requestor_id": "sup-1",
        })
        client.post("/api/tasks/task-1/start", json={"user_id": "stu-1"})
        r = client.post("/api/tasks/task-1/complete", json={"user_id": "stu-1"})
        assert r.status_code == 200
        assert r.json()["status"] == "COMPLETED"

    def test_delete_task_204(self, client):
        setup_all(client)
        r = client.delete("/api/tasks/task-1?requestor_id=sup-1")
        assert r.status_code == 204

    def test_delete_inprogress_task_422(self, client):
        setup_all(client)
        client.post("/api/tasks/task-1/assign", json={
            "assignee_id": "stu-1", "requestor_id": "sup-1",
        })
        client.post("/api/tasks/task-1/start", json={"user_id": "stu-1"})
        r = client.delete("/api/tasks/task-1?requestor_id=sup-1")
        assert r.status_code == 422
