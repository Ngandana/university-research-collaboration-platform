"""
tests/services/test_services.py
Unit tests for UserService, ProjectService, and TaskService.
Run: python -m pytest tests/services/test_services.py -v
"""

import sys, os
from datetime import date, timedelta
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

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
from src.user import UserRole, UserStatus
from src.research_project import ProjectStatus
from src.task import TaskStatus


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def user_repo():
    return RepositoryFactory.get_user_repository(STORAGE_MEMORY)

@pytest.fixture
def project_repo():
    return RepositoryFactory.get_project_repository(STORAGE_MEMORY)

@pytest.fixture
def task_repo():
    return RepositoryFactory.get_task_repository(STORAGE_MEMORY)

@pytest.fixture
def user_svc(user_repo):
    return UserService(user_repo)

@pytest.fixture
def project_svc(project_repo, user_repo):
    return ProjectService(project_repo, user_repo)

@pytest.fixture
def task_svc(task_repo, user_repo, project_repo):
    return TaskService(task_repo, user_repo, project_repo)

@pytest.fixture
def supervisor(user_svc):
    return user_svc.register_user(
        "sup-1", "Prof Nkosi", "nkosi@uni.ac.za", "securepass", "supervisor"
    )

@pytest.fixture
def student(user_svc):
    return user_svc.register_user(
        "stu-1", "Alice Dube", "alice@uni.ac.za", "securepass", "student"
    )

@pytest.fixture
def active_project(project_svc, supervisor):
    return project_svc.create_project(
        "proj-1", "AI Research", "Exploring AI", supervisor.user_id
    )

@pytest.fixture
def future_date():
    return date.today() + timedelta(days=14)


# ════════════════════════════════════════════════════════════════════════════
# UserService Tests
# ════════════════════════════════════════════════════════════════════════════

class TestUserService:

    def test_register_user_success(self, user_svc):
        user = user_svc.register_user("u1", "Test", "t@u.ac.za", "pass123", "student")
        assert user.role == UserRole.STUDENT
        assert user.status == UserStatus.ACTIVE

    def test_register_duplicate_email_raises(self, user_svc):
        user_svc.register_user("u1", "Test", "same@u.ac.za", "pass123", "student")
        with pytest.raises(DuplicateEmailError):
            user_svc.register_user("u2", "Test2", "same@u.ac.za", "pass123", "student")

    def test_register_invalid_role_raises(self, user_svc):
        with pytest.raises(InvalidRoleError):
            user_svc.register_user("u1", "T", "t@u.ac.za", "pass123", "hacker")

    def test_register_short_password_raises(self, user_svc):
        with pytest.raises(ValueError, match="6 characters"):
            user_svc.register_user("u1", "T", "t@u.ac.za", "abc", "student")

    def test_register_empty_name_raises(self, user_svc):
        with pytest.raises(ValueError, match="Name"):
            user_svc.register_user("u1", "  ", "t@u.ac.za", "pass123", "student")

    def test_register_invalid_email_raises(self, user_svc):
        with pytest.raises(ValueError, match="email"):
            user_svc.register_user("u1", "T", "notanemail", "pass123", "student")

    def test_get_user_found(self, user_svc, supervisor):
        result = user_svc.get_user(supervisor.user_id)
        assert result.user_id == supervisor.user_id

    def test_get_user_not_found_raises(self, user_svc):
        with pytest.raises(UserNotFoundError):
            user_svc.get_user("nonexistent")

    def test_get_all_users(self, user_svc, supervisor, student):
        users = user_svc.get_all_users()
        assert len(users) == 2

    def test_get_users_by_role(self, user_svc, supervisor, student):
        supervisors = user_svc.get_users_by_role("supervisor")
        assert len(supervisors) == 1
        assert supervisors[0].user_id == supervisor.user_id

    def test_update_profile_name(self, user_svc, student):
        updated = user_svc.update_profile(student.user_id, name="Alice Updated")
        assert updated.name == "Alice Updated"

    def test_update_profile_email_duplicate_raises(self, user_svc, supervisor, student):
        with pytest.raises(DuplicateEmailError):
            user_svc.update_profile(student.user_id, email=supervisor.email)

    def test_suspend_user(self, user_svc, student):
        user_svc.suspend_user(student.user_id)
        assert user_svc.get_user(student.user_id).status == UserStatus.SUSPENDED

    def test_suspend_already_suspended_raises(self, user_svc, student):
        user_svc.suspend_user(student.user_id)
        with pytest.raises(UserNotActiveError):
            user_svc.suspend_user(student.user_id)

    def test_reactivate_user(self, user_svc, student):
        user_svc.suspend_user(student.user_id)
        user_svc.reactivate_user(student.user_id)
        assert user_svc.get_user(student.user_id).status == UserStatus.ACTIVE

    def test_reactivate_active_user_raises(self, user_svc, student):
        with pytest.raises(ValueError, match="not suspended"):
            user_svc.reactivate_user(student.user_id)

    def test_deactivate_user(self, user_svc, student):
        user_svc.deactivate_user(student.user_id)
        assert user_svc.get_user(student.user_id).status == UserStatus.DEACTIVATED

    def test_duplicate_user_id_raises(self, user_svc):
        user_svc.register_user("u1", "T", "t@u.ac.za", "pass123", "student")
        with pytest.raises(ValueError, match="already in use"):
            user_svc.register_user("u1", "T2", "t2@u.ac.za", "pass123", "student")


# ════════════════════════════════════════════════════════════════════════════
# ProjectService Tests
# ════════════════════════════════════════════════════════════════════════════

class TestProjectService:

    def test_create_project_success(self, project_svc, supervisor):
        project = project_svc.create_project(
            "p1", "Test Project", "Desc", supervisor.user_id
        )
        assert project.status == ProjectStatus.ACTIVE
        assert project.owner.user_id == supervisor.user_id

    def test_create_project_student_owner_raises(self, project_svc, student):
        with pytest.raises(UnauthorizedError, match="role"):
            project_svc.create_project("p1", "Test", "Desc", student.user_id)

    def test_create_project_nonexistent_owner_raises(self, project_svc):
        with pytest.raises(Exception, match="not found"):
            project_svc.create_project("p1", "Test", "Desc", "nobody")

    def test_create_project_empty_title_raises(self, project_svc, supervisor):
        with pytest.raises(ValueError, match="title"):
            project_svc.create_project("p1", "  ", "Desc", supervisor.user_id)

    def test_create_project_duplicate_id_raises(self, project_svc, supervisor):
        project_svc.create_project("p1", "First", "Desc", supervisor.user_id)
        with pytest.raises(ValueError, match="already in use"):
            project_svc.create_project("p1", "Second", "Desc", supervisor.user_id)

    def test_get_project_found(self, project_svc, active_project):
        result = project_svc.get_project(active_project.project_id)
        assert result.project_id == active_project.project_id

    def test_get_project_not_found_raises(self, project_svc):
        with pytest.raises(ProjectNotFoundError):
            project_svc.get_project("ghost")

    def test_get_all_projects(self, project_svc, active_project):
        assert len(project_svc.get_all_projects()) == 1

    def test_get_projects_by_owner(self, project_svc, active_project, supervisor):
        results = project_svc.get_projects_by_owner(supervisor.user_id)
        assert active_project in results

    def test_add_member_success(self, project_svc, active_project, student, supervisor):
        project = project_svc.add_member(
            active_project.project_id, student.user_id, supervisor.user_id
        )
        assert student in project.get_members()

    def test_add_member_wrong_requestor_raises(self, project_svc, active_project, student):
        with pytest.raises(UnauthorizedError, match="owner"):
            project_svc.add_member(
                active_project.project_id, student.user_id, student.user_id
            )

    def test_complete_project(self, project_svc, active_project, supervisor):
        project = project_svc.complete_project(
            active_project.project_id, supervisor.user_id
        )
        assert project.status == ProjectStatus.COMPLETED

    def test_complete_project_wrong_requestor_raises(self, project_svc,
                                                      active_project, student):
        with pytest.raises(UnauthorizedError):
            project_svc.complete_project(active_project.project_id, student.user_id)

    def test_complete_already_completed_raises(self, project_svc,
                                               active_project, supervisor):
        project_svc.complete_project(active_project.project_id, supervisor.user_id)
        with pytest.raises(ProjectStateError):
            project_svc.complete_project(active_project.project_id, supervisor.user_id)

    def test_archive_completed_project(self, project_svc, active_project, supervisor):
        project_svc.complete_project(active_project.project_id, supervisor.user_id)
        project = project_svc.archive_project(active_project.project_id)
        assert project.status == ProjectStatus.ARCHIVED

    def test_archive_active_project_raises(self, project_svc, active_project):
        with pytest.raises(ProjectStateError):
            project_svc.archive_project(active_project.project_id)

    def test_delete_project_active_raises(self, project_svc, active_project, supervisor):
        with pytest.raises(ProjectStateError, match="ACTIVE"):
            project_svc.delete_project(active_project.project_id, supervisor.user_id)

    def test_delete_completed_project(self, project_svc, active_project, supervisor):
        project_svc.complete_project(active_project.project_id, supervisor.user_id)
        project_svc.delete_project(active_project.project_id, supervisor.user_id)
        with pytest.raises(ProjectNotFoundError):
            project_svc.get_project(active_project.project_id)


# ════════════════════════════════════════════════════════════════════════════
# TaskService Tests
# ════════════════════════════════════════════════════════════════════════════

class TestTaskService:

    def test_create_task_success(self, task_svc, active_project,
                                  supervisor, future_date):
        task = task_svc.create_task(
            "t1", "Literature Review", "Read papers",
            future_date, active_project.project_id, supervisor.user_id,
        )
        assert task.status == TaskStatus.CREATED
        assert task.title == "Literature Review"

    def test_create_task_student_creator_raises(self, task_svc, active_project,
                                                 student, future_date):
        with pytest.raises(TaskUnauthorizedError, match="Supervisors"):
            task_svc.create_task(
                "t1", "Task", "Desc", future_date,
                active_project.project_id, student.user_id,
            )

    def test_create_task_past_deadline_raises(self, task_svc, active_project, supervisor):
        with pytest.raises(ValueError, match="future"):
            task_svc.create_task(
                "t1", "Late", "Desc",
                date.today() - timedelta(days=1),
                active_project.project_id, supervisor.user_id,
            )

    def test_create_task_empty_title_raises(self, task_svc, active_project,
                                             supervisor, future_date):
        with pytest.raises(ValueError, match="title"):
            task_svc.create_task(
                "t1", "  ", "Desc", future_date,
                active_project.project_id, supervisor.user_id,
            )

    def test_create_task_nonexistent_project_raises(self, task_svc,
                                                     supervisor, future_date):
        with pytest.raises(Exception, match="not found"):
            task_svc.create_task(
                "t1", "Task", "Desc", future_date, "ghost-project", supervisor.user_id,
            )

    def test_get_task_found(self, task_svc, active_project, supervisor, future_date):
        task = task_svc.create_task(
            "t1", "Task", "Desc", future_date,
            active_project.project_id, supervisor.user_id,
        )
        assert task_svc.get_task("t1").task_id == "t1"

    def test_get_task_not_found_raises(self, task_svc):
        with pytest.raises(TaskNotFoundError):
            task_svc.get_task("ghost")

    def test_assign_task_success(self, task_svc, active_project,
                                  supervisor, student, future_date):
        task = task_svc.create_task(
            "t1", "Task", "Desc", future_date,
            active_project.project_id, supervisor.user_id,
        )
        assigned = task_svc.assign_task("t1", student.user_id, supervisor.user_id)
        assert assigned.status == TaskStatus.ASSIGNED
        assert assigned.assigned_to.user_id == student.user_id

    def test_assign_task_student_requestor_raises(self, task_svc, active_project,
                                                   supervisor, student, future_date):
        task_svc.create_task(
            "t1", "Task", "Desc", future_date,
            active_project.project_id, supervisor.user_id,
        )
        with pytest.raises(TaskUnauthorizedError):
            task_svc.assign_task("t1", student.user_id, student.user_id)

    def test_start_task_success(self, task_svc, active_project,
                                 supervisor, student, future_date):
        task_svc.create_task(
            "t1", "Task", "Desc", future_date,
            active_project.project_id, supervisor.user_id,
        )
        task_svc.assign_task("t1", student.user_id, supervisor.user_id)
        started = task_svc.start_task("t1", student.user_id)
        assert started.status == TaskStatus.IN_PROGRESS

    def test_start_task_wrong_user_raises(self, task_svc, active_project,
                                           supervisor, student, future_date):
        task_svc.create_task(
            "t1", "Task", "Desc", future_date,
            active_project.project_id, supervisor.user_id,
        )
        task_svc.assign_task("t1", student.user_id, supervisor.user_id)
        with pytest.raises(TaskUnauthorizedError):
            task_svc.start_task("t1", supervisor.user_id)

    def test_complete_task_success(self, task_svc, active_project,
                                    supervisor, student, future_date):
        task_svc.create_task(
            "t1", "Task", "Desc", future_date,
            active_project.project_id, supervisor.user_id,
        )
        task_svc.assign_task("t1", student.user_id, supervisor.user_id)
        task_svc.start_task("t1", student.user_id)
        completed = task_svc.complete_task("t1", student.user_id)
        assert completed.status == TaskStatus.COMPLETED

    def test_active_task_limit_enforced(self, task_svc, active_project,
                                         supervisor, student, future_date,
                                         user_repo):
        # Fill up to the max
        for i in range(TaskService.MAX_ACTIVE_TASKS_PER_STUDENT):
            task_svc.create_task(
                f"t{i}", f"Task {i}", "Desc", future_date,
                active_project.project_id, supervisor.user_id,
            )
            task_svc.assign_task(f"t{i}", student.user_id, supervisor.user_id)

        # The (MAX+1)th assignment should fail
        task_svc.create_task(
            "t-extra", "Extra Task", "Desc", future_date,
            active_project.project_id, supervisor.user_id,
        )
        with pytest.raises(TaskStateError, match="active tasks"):
            task_svc.assign_task("t-extra", student.user_id, supervisor.user_id)

    def test_delete_created_task(self, task_svc, active_project,
                                  supervisor, future_date):
        task_svc.create_task(
            "t1", "Task", "Desc", future_date,
            active_project.project_id, supervisor.user_id,
        )
        task_svc.delete_task("t1", supervisor.user_id)
        with pytest.raises(TaskNotFoundError):
            task_svc.get_task("t1")

    def test_delete_inprogress_task_raises(self, task_svc, active_project,
                                            supervisor, student, future_date):
        task_svc.create_task(
            "t1", "Task", "Desc", future_date,
            active_project.project_id, supervisor.user_id,
        )
        task_svc.assign_task("t1", student.user_id, supervisor.user_id)
        task_svc.start_task("t1", student.user_id)
        with pytest.raises(TaskStateError):
            task_svc.delete_task("t1", supervisor.user_id)
