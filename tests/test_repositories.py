"""
test_repositories.py
Unit tests for the repository layer — all in-memory implementations
and the RepositoryFactory abstraction mechanism.

Run: pytest tests/test_repositories.py -v
"""

import sys
import os
from datetime import date, timedelta
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.user import User, UserRole, UserStatus
from src.research_project import ResearchProject, ProjectStatus
from src.document import Document, DocumentStatus
from src.task import Task, TaskStatus
from src.communication import Message, MessageStatus, Invitation, InvitationStatus
from creational_patterns.simple_factory import UserFactory

from repositories.inmemory.implementations import (
    InMemoryUserRepository,
    InMemoryResearchProjectRepository,
    InMemoryDocumentRepository,
    InMemoryTaskRepository,
    InMemoryMessageRepository,
    InMemoryInvitationRepository,
)
from factories.repository_factory import RepositoryFactory, STORAGE_MEMORY


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def supervisor():
    u = UserFactory.create_user("sup-1", "Prof Nkosi",
                                "nkosi@uni.ac.za", "pw", "supervisor")
    u.register()
    return u


@pytest.fixture
def student():
    u = UserFactory.create_user("stu-1", "Alice Dube",
                                "alice@uni.ac.za", "pw", "student")
    u.register()
    return u


@pytest.fixture
def student2():
    u = UserFactory.create_user("stu-2", "Bob Mokoena",
                                "bob@uni.ac.za", "pw", "student")
    u.register()
    return u


@pytest.fixture
def active_project(supervisor):
    p = ResearchProject("proj-1", "AI Research",
                        "Exploring AI applications", supervisor)
    p.activate()
    return p


@pytest.fixture
def user_repo():
    return InMemoryUserRepository()


@pytest.fixture
def project_repo():
    return InMemoryResearchProjectRepository()


@pytest.fixture
def document_repo():
    return InMemoryDocumentRepository()


@pytest.fixture
def task_repo():
    return InMemoryTaskRepository()


@pytest.fixture
def message_repo():
    return InMemoryMessageRepository()


@pytest.fixture
def invitation_repo():
    return InMemoryInvitationRepository()


# ════════════════════════════════════════════════════════════════════════════
# 1. UserRepository Tests
# ════════════════════════════════════════════════════════════════════════════

class TestInMemoryUserRepository:

    def test_save_and_find_by_id(self, user_repo, supervisor):
        user_repo.save(supervisor)
        result = user_repo.find_by_id("sup-1")
        assert result is supervisor

    def test_find_by_id_missing_returns_none(self, user_repo):
        assert user_repo.find_by_id("nonexistent") is None

    def test_find_all_returns_all_users(self, user_repo, supervisor, student):
        user_repo.save(supervisor)
        user_repo.save(student)
        all_users = user_repo.find_all()
        assert len(all_users) == 2
        assert supervisor in all_users
        assert student in all_users

    def test_find_all_empty_returns_empty_list(self, user_repo):
        assert user_repo.find_all() == []

    def test_delete_removes_user(self, user_repo, supervisor):
        user_repo.save(supervisor)
        user_repo.delete("sup-1")
        assert user_repo.find_by_id("sup-1") is None

    def test_delete_nonexistent_no_error(self, user_repo):
        user_repo.delete("ghost")  # should not raise

    def test_exists_true(self, user_repo, supervisor):
        user_repo.save(supervisor)
        assert user_repo.exists("sup-1") is True

    def test_exists_false(self, user_repo):
        assert user_repo.exists("nobody") is False

    def test_count(self, user_repo, supervisor, student):
        assert user_repo.count() == 0
        user_repo.save(supervisor)
        assert user_repo.count() == 1
        user_repo.save(student)
        assert user_repo.count() == 2

    def test_save_overwrites_existing(self, user_repo, supervisor):
        user_repo.save(supervisor)
        supervisor.update_profile(name="Prof Nkosi Updated")
        user_repo.save(supervisor)
        result = user_repo.find_by_id("sup-1")
        assert result.name == "Prof Nkosi Updated"
        assert user_repo.count() == 1  # no duplicate

    def test_find_by_email_found(self, user_repo, supervisor):
        user_repo.save(supervisor)
        result = user_repo.find_by_email("nkosi@uni.ac.za")
        assert result is supervisor

    def test_find_by_email_not_found(self, user_repo):
        assert user_repo.find_by_email("unknown@uni.ac.za") is None

    def test_find_by_role(self, user_repo, supervisor, student, student2):
        user_repo.save(supervisor)
        user_repo.save(student)
        user_repo.save(student2)
        students = user_repo.find_by_role(UserRole.STUDENT)
        supervisors = user_repo.find_by_role(UserRole.SUPERVISOR)
        assert len(students) == 2
        assert len(supervisors) == 1
        assert supervisor in supervisors

    def test_find_by_status_active(self, user_repo, supervisor, student):
        user_repo.save(supervisor)
        user_repo.save(student)
        active = user_repo.find_by_status(UserStatus.ACTIVE)
        assert len(active) == 2

    def test_find_by_status_suspended(self, user_repo, student):
        student.suspend()
        user_repo.save(student)
        suspended = user_repo.find_by_status(UserStatus.SUSPENDED)
        assert student in suspended

    def test_find_all_returns_copy(self, user_repo, supervisor):
        user_repo.save(supervisor)
        result = user_repo.find_all()
        result.clear()
        assert user_repo.count() == 1  # internal store not affected


# ════════════════════════════════════════════════════════════════════════════
# 2. ResearchProjectRepository Tests
# ════════════════════════════════════════════════════════════════════════════

class TestInMemoryResearchProjectRepository:

    def test_save_and_find_by_id(self, project_repo, active_project):
        project_repo.save(active_project)
        result = project_repo.find_by_id("proj-1")
        assert result is active_project

    def test_find_by_id_missing(self, project_repo):
        assert project_repo.find_by_id("x") is None

    def test_delete(self, project_repo, active_project):
        project_repo.save(active_project)
        project_repo.delete("proj-1")
        assert project_repo.find_by_id("proj-1") is None

    def test_exists(self, project_repo, active_project):
        project_repo.save(active_project)
        assert project_repo.exists("proj-1") is True
        assert project_repo.exists("ghost") is False

    def test_count(self, project_repo, supervisor):
        assert project_repo.count() == 0
        p1 = ResearchProject("p1", "T1", "d", supervisor)
        p2 = ResearchProject("p2", "T2", "d", supervisor)
        project_repo.save(p1)
        project_repo.save(p2)
        assert project_repo.count() == 2

    def test_find_by_owner(self, project_repo, supervisor):
        p1 = ResearchProject("p1", "T1", "d", supervisor)
        p2 = ResearchProject("p2", "T2", "d", supervisor)
        project_repo.save(p1)
        project_repo.save(p2)
        results = project_repo.find_by_owner("sup-1")
        assert len(results) == 2

    def test_find_by_owner_no_match(self, project_repo, active_project):
        project_repo.save(active_project)
        assert project_repo.find_by_owner("other-user") == []

    def test_find_by_status(self, project_repo, supervisor):
        p1 = ResearchProject("p1", "T1", "d", supervisor)
        p2 = ResearchProject("p2", "T2", "d", supervisor)
        p1.activate()
        project_repo.save(p1)
        project_repo.save(p2)
        active = project_repo.find_by_status(ProjectStatus.ACTIVE)
        created = project_repo.find_by_status(ProjectStatus.CREATED)
        assert p1 in active
        assert p2 in created

    def test_find_by_member(self, project_repo, active_project, student):
        active_project.add_member(student)
        project_repo.save(active_project)
        results = project_repo.find_by_member("stu-1")
        assert active_project in results

    def test_find_by_member_not_in_project(self, project_repo, active_project):
        project_repo.save(active_project)
        assert project_repo.find_by_member("stu-99") == []


# ════════════════════════════════════════════════════════════════════════════
# 3. DocumentRepository Tests
# ════════════════════════════════════════════════════════════════════════════

class TestInMemoryDocumentRepository:

    def test_save_and_find_by_id(self, document_repo, student):
        doc = Document("doc-1", "Proposal", student)
        document_repo.save(doc)
        assert document_repo.find_by_id("doc-1") is doc

    def test_delete(self, document_repo, student):
        doc = Document("doc-1", "Proposal", student)
        document_repo.save(doc)
        document_repo.delete("doc-1")
        assert document_repo.find_by_id("doc-1") is None

    def test_find_by_project(self, document_repo, student):
        doc1 = Document("d1", "Doc1", student)
        doc2 = Document("d2", "Doc2", student)
        document_repo.save_for_project(doc1, "proj-1", "stu-1")
        document_repo.save_for_project(doc2, "proj-2", "stu-1")
        results = document_repo.find_by_project("proj-1")
        assert doc1 in results
        assert doc2 not in results

    def test_find_by_uploader(self, document_repo, student, student2):
        doc1 = Document("d1", "Doc1", student)
        doc2 = Document("d2", "Doc2", student2)
        document_repo.save_for_project(doc1, "p1", "stu-1")
        document_repo.save_for_project(doc2, "p1", "stu-2")
        results = document_repo.find_by_uploader("stu-1")
        assert doc1 in results
        assert doc2 not in results

    def test_find_by_status(self, document_repo, student):
        doc = Document("d1", "Doc", student)
        doc.upload("file.pdf", "pdf", 1.0, "v1")
        document_repo.save(doc)
        stored = document_repo.find_by_status(DocumentStatus.STORED)
        assert doc in stored

    def test_count(self, document_repo, student):
        assert document_repo.count() == 0
        document_repo.save(Document("d1", "A", student))
        document_repo.save(Document("d2", "B", student))
        assert document_repo.count() == 2


# ════════════════════════════════════════════════════════════════════════════
# 4. TaskRepository Tests
# ════════════════════════════════════════════════════════════════════════════

class TestInMemoryTaskRepository:

    def test_save_and_find_by_id(self, task_repo, supervisor):
        task = Task("t1", "Review", "Do it",
                    date.today() + timedelta(days=7), supervisor)
        task_repo.save(task)
        assert task_repo.find_by_id("t1") is task

    def test_delete(self, task_repo, supervisor):
        task = Task("t1", "Review", "Do it",
                    date.today() + timedelta(days=7), supervisor)
        task_repo.save(task)
        task_repo.delete("t1")
        assert task_repo.find_by_id("t1") is None

    def test_find_by_project(self, task_repo, supervisor):
        t1 = Task("t1", "T1", "d", date.today() + timedelta(7), supervisor)
        t2 = Task("t2", "T2", "d", date.today() + timedelta(7), supervisor)
        task_repo.save_for_project(t1, "proj-1")
        task_repo.save_for_project(t2, "proj-2")
        results = task_repo.find_by_project("proj-1")
        assert t1 in results
        assert t2 not in results

    def test_find_by_assignee(self, task_repo, supervisor, student):
        t1 = Task("t1", "T1", "d", date.today() + timedelta(7), supervisor)
        t2 = Task("t2", "T2", "d", date.today() + timedelta(7), supervisor)
        t1.assign(student)
        task_repo.save(t1)
        task_repo.save(t2)
        results = task_repo.find_by_assignee("stu-1")
        assert t1 in results
        assert t2 not in results

    def test_find_by_status(self, task_repo, supervisor, student):
        t1 = Task("t1", "T1", "d", date.today() + timedelta(7), supervisor)
        t2 = Task("t2", "T2", "d", date.today() + timedelta(7), supervisor)
        t1.assign(student)
        task_repo.save(t1)
        task_repo.save(t2)
        assigned = task_repo.find_by_status(TaskStatus.ASSIGNED)
        created = task_repo.find_by_status(TaskStatus.CREATED)
        assert t1 in assigned
        assert t2 in created

    def test_find_overdue(self, task_repo, supervisor, student):
        past = date.today() - timedelta(days=1)
        t = Task("t1", "Late", "d", past, supervisor)
        t.assign(student)
        t.mark_overdue()
        task_repo.save(t)
        overdue = task_repo.find_overdue()
        assert t in overdue

    def test_count(self, task_repo, supervisor):
        assert task_repo.count() == 0
        task_repo.save(Task("t1", "A", "d",
                            date.today() + timedelta(1), supervisor))
        assert task_repo.count() == 1


# ════════════════════════════════════════════════════════════════════════════
# 5. MessageRepository Tests
# ════════════════════════════════════════════════════════════════════════════

class TestInMemoryMessageRepository:

    def test_save_and_find_by_id(self, message_repo, supervisor, student):
        msg = Message("m1", "Hello!", supervisor, student)
        message_repo.save(msg)
        assert message_repo.find_by_id("m1") is msg

    def test_delete(self, message_repo, supervisor, student):
        msg = Message("m1", "Hello!", supervisor, student)
        message_repo.save(msg)
        message_repo.delete("m1")
        assert message_repo.find_by_id("m1") is None

    def test_find_by_sender(self, message_repo, supervisor, student):
        msg = Message("m1", "Hi", supervisor, student)
        message_repo.save(msg)
        results = message_repo.find_by_sender("sup-1")
        assert msg in results

    def test_find_by_recipient(self, message_repo, supervisor, student):
        msg = Message("m1", "Review please", supervisor, student)
        message_repo.save(msg)
        results = message_repo.find_by_recipient("stu-1")
        assert msg in results

    def test_find_unread(self, message_repo, supervisor, student):
        msg = Message("m1", "Unread msg", supervisor, student)
        msg.send()
        msg.deliver()
        message_repo.save(msg)
        unread = message_repo.find_unread("stu-1")
        assert msg in unread

    def test_find_unread_excludes_read(self, message_repo, supervisor, student):
        msg = Message("m1", "Read msg", supervisor, student)
        msg.send()
        msg.deliver()
        msg.mark_read()
        message_repo.save(msg)
        unread = message_repo.find_unread("stu-1")
        assert msg not in unread

    def test_count(self, message_repo, supervisor, student):
        assert message_repo.count() == 0
        message_repo.save(Message("m1", "Hi", supervisor, student))
        assert message_repo.count() == 1


# ════════════════════════════════════════════════════════════════════════════
# 6. InvitationRepository Tests
# ════════════════════════════════════════════════════════════════════════════

class TestInMemoryInvitationRepository:

    def test_save_and_find_by_id(self, invitation_repo, supervisor,
                                  student, active_project):
        inv = Invitation("inv-1", supervisor, student, active_project)
        invitation_repo.save(inv)
        assert invitation_repo.find_by_id("inv-1") is inv

    def test_delete(self, invitation_repo, supervisor, student, active_project):
        inv = Invitation("inv-1", supervisor, student, active_project)
        invitation_repo.save(inv)
        invitation_repo.delete("inv-1")
        assert invitation_repo.find_by_id("inv-1") is None

    def test_find_by_project(self, invitation_repo, supervisor,
                              student, student2, active_project):
        inv1 = Invitation("inv-1", supervisor, student, active_project)
        inv2 = Invitation("inv-2", supervisor, student2, active_project)
        invitation_repo.save(inv1)
        invitation_repo.save(inv2)
        results = invitation_repo.find_by_project("proj-1")
        assert inv1 in results
        assert inv2 in results

    def test_find_by_recipient(self, invitation_repo, supervisor,
                                student, active_project):
        inv = Invitation("inv-1", supervisor, student, active_project)
        invitation_repo.save(inv)
        results = invitation_repo.find_by_recipient("stu-1")
        assert inv in results

    def test_find_pending(self, invitation_repo, supervisor,
                           student, student2, active_project):
        inv1 = Invitation("inv-1", supervisor, student, active_project)
        inv2 = Invitation("inv-2", supervisor, student2, active_project)
        inv2.reject()
        invitation_repo.save(inv1)
        invitation_repo.save(inv2)
        pending = invitation_repo.find_pending("stu-1")
        assert inv1 in pending
        pending2 = invitation_repo.find_pending("stu-2")
        assert inv2 not in pending2

    def test_count(self, invitation_repo, supervisor, student, active_project):
        assert invitation_repo.count() == 0
        invitation_repo.save(
            Invitation("inv-1", supervisor, student, active_project))
        assert invitation_repo.count() == 1


# ════════════════════════════════════════════════════════════════════════════
# 7. RepositoryFactory Tests
# ════════════════════════════════════════════════════════════════════════════

class TestRepositoryFactory:

    def test_get_user_repository_memory(self):
        repo = RepositoryFactory.get_user_repository(STORAGE_MEMORY)
        assert isinstance(repo, InMemoryUserRepository)

    def test_get_project_repository_memory(self):
        repo = RepositoryFactory.get_project_repository(STORAGE_MEMORY)
        assert isinstance(repo, InMemoryResearchProjectRepository)

    def test_get_document_repository_memory(self):
        repo = RepositoryFactory.get_document_repository(STORAGE_MEMORY)
        assert isinstance(repo, InMemoryDocumentRepository)

    def test_get_task_repository_memory(self):
        repo = RepositoryFactory.get_task_repository(STORAGE_MEMORY)
        assert isinstance(repo, InMemoryTaskRepository)

    def test_get_message_repository_memory(self):
        repo = RepositoryFactory.get_message_repository(STORAGE_MEMORY)
        assert isinstance(repo, InMemoryMessageRepository)

    def test_get_invitation_repository_memory(self):
        repo = RepositoryFactory.get_invitation_repository(STORAGE_MEMORY)
        assert isinstance(repo, InMemoryInvitationRepository)

    def test_invalid_storage_type_raises(self):
        with pytest.raises(ValueError, match="Unknown storage type"):
            RepositoryFactory.get_user_repository("REDIS")

    def test_case_insensitive_storage_type(self):
        repo = RepositoryFactory.get_user_repository("memory")
        assert isinstance(repo, InMemoryUserRepository)

    def test_filesystem_returns_stub_for_user(self):
        from repositories.stubs import FileSystemUserRepository
        repo = RepositoryFactory.get_user_repository("FILESYSTEM")
        assert isinstance(repo, FileSystemUserRepository)

    def test_filesystem_stub_raises_on_use(self):
        repo = RepositoryFactory.get_user_repository("FILESYSTEM")
        with pytest.raises(NotImplementedError):
            repo.save(None)

    def test_database_returns_stub_for_user(self):
        from repositories.stubs import DatabaseUserRepository
        repo = RepositoryFactory.get_user_repository("DATABASE")
        assert isinstance(repo, DatabaseUserRepository)

    def test_database_stub_raises_on_use(self):
        repo = RepositoryFactory.get_user_repository("DATABASE")
        with pytest.raises(NotImplementedError):
            repo.find_by_id("u1")

    def test_factory_produces_independent_instances(self):
        repo1 = RepositoryFactory.get_user_repository(STORAGE_MEMORY)
        repo2 = RepositoryFactory.get_user_repository(STORAGE_MEMORY)
        assert repo1 is not repo2  # each call gives a fresh instance

    def test_document_unsupported_backend_raises(self):
        with pytest.raises(NotImplementedError):
            RepositoryFactory.get_document_repository("FILESYSTEM")
