"""
test_creational_patterns.py
Unit tests for all six creational patterns.
Run with:  pytest tests/ -v --tb=short
Coverage:  pytest tests/ --cov=creational_patterns --cov=src --cov-report=term-missing
"""

import sys
import os
import threading
from datetime import date, timedelta
import pytest

# Ensure project root is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.user import User, UserRole, UserStatus
from src.task import Task, TaskStatus
from src.document import Document, DocumentStatus
from src.research_project import ResearchProject, ProjectStatus
from src.communication import (Message, MessageStatus,
                                Notification, NotificationType,
                                Invitation, InvitationStatus)

from creational_patterns.simple_factory import UserFactory
from creational_patterns.factory_method import (
    TaskUpdateNotificationCreator,
    MessageReceivedNotificationCreator,
    ProjectUpdateNotificationCreator,
)
from creational_patterns.abstract_factory import (
    LocalStorageFactory, CloudStorageFactory, upload_document,
)
from creational_patterns.builder import ResearchProjectBuilder, ProjectDirector
from creational_patterns.prototype import TaskPrototype, TaskCache, build_default_task_cache
from creational_patterns.singleton import DatabaseConnection


# ════════════════════════════════════════════════════════════════════════════
# Fixtures
# ════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def active_supervisor():
    u = UserFactory.create_user("sup-1", "Prof Nkosi",
                                "nkosi@uni.ac.za", "secure", "supervisor")
    u.register()
    return u


@pytest.fixture
def active_student():
    u = UserFactory.create_user("stu-1", "Alice Dube",
                                "alice@uni.ac.za", "pass123", "student")
    u.register()
    return u


@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset the DB singleton before every test that touches it."""
    DatabaseConnection._reset_instance()
    yield
    DatabaseConnection._reset_instance()


# ════════════════════════════════════════════════════════════════════════════
# 1. SIMPLE FACTORY TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestSimpleFactory:

    def test_creates_student(self):
        user = UserFactory.create_user("u1", "Alice", "a@u.ac.za",
                                       "pw", "student")
        assert user.role == UserRole.STUDENT

    def test_creates_supervisor(self):
        user = UserFactory.create_user("u2", "Prof", "p@u.ac.za",
                                       "pw", "supervisor")
        assert user.role == UserRole.SUPERVISOR

    def test_creates_researcher(self):
        user = UserFactory.create_user("u3", "Dr Smith", "s@u.ac.za",
                                       "pw", "researcher")
        assert user.role == UserRole.RESEARCHER

    def test_creates_admin(self):
        user = UserFactory.create_user("u4", "Admin", "a@u.ac.za",
                                       "pw", "admin")
        assert user.role == UserRole.ADMIN

    def test_case_insensitive_role(self):
        user = UserFactory.create_user("u5", "Test", "t@u.ac.za",
                                       "pw", "SUPERVISOR")
        assert user.role == UserRole.SUPERVISOR

    def test_initial_status_is_registered(self):
        user = UserFactory.create_user("u6", "Test", "t@u.ac.za",
                                       "pw", "student")
        assert user.status == UserStatus.REGISTERED

    def test_invalid_role_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown role"):
            UserFactory.create_user("u7", "Bad", "b@u.ac.za",
                                    "pw", "hacker")

    def test_empty_role_raises_value_error(self):
        with pytest.raises(ValueError):
            UserFactory.create_user("u8", "Bad", "b@u.ac.za", "pw", "")

    def test_password_is_hashed(self):
        user = UserFactory.create_user("u9", "Test", "t@u.ac.za",
                                       "mypassword", "student")
        assert user._password_hash != "mypassword"

    def test_login_correct_password(self):
        user = UserFactory.create_user("u10", "T", "t@u.ac.za",
                                       "correct", "student")
        user.register()
        assert user.login("correct") is True

    def test_login_wrong_password(self):
        user = UserFactory.create_user("u11", "T", "t@u.ac.za",
                                       "correct", "student")
        user.register()
        assert user.login("wrong") is False


# ════════════════════════════════════════════════════════════════════════════
# 2. FACTORY METHOD TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestFactoryMethod:

    def test_task_update_notification_type(self, active_student):
        creator = TaskUpdateNotificationCreator()
        notif = creator.notify(active_student, "Task overdue")
        assert notif.notification_type == NotificationType.TASK_UPDATE

    def test_message_received_notification_type(self, active_student):
        creator = MessageReceivedNotificationCreator()
        notif = creator.notify(active_student, "Prof Nkosi")
        assert notif.notification_type == NotificationType.MESSAGE_RECEIVED

    def test_project_update_notification_type(self, active_student):
        creator = ProjectUpdateNotificationCreator()
        notif = creator.notify(active_student, "Project archived")
        assert notif.notification_type == NotificationType.PROJECT_UPDATE

    def test_notification_recipient_is_correct(self, active_student):
        creator = TaskUpdateNotificationCreator()
        notif = creator.notify(active_student, "Test")
        assert notif.recipient is active_student

    def test_notification_initially_unread(self, active_student):
        creator = MessageReceivedNotificationCreator()
        notif = creator.notify(active_student, "Someone")
        assert notif.is_read is False

    def test_notification_message_contains_context(self, active_student):
        creator = TaskUpdateNotificationCreator()
        notif = creator.notify(active_student, "Literature Review overdue")
        assert "Literature Review overdue" in notif.message

    def test_mark_read(self, active_student):
        creator = ProjectUpdateNotificationCreator()
        notif = creator.notify(active_student, "Project completed")
        notif.mark_read()
        assert notif.is_read is True

    def test_each_creator_produces_unique_ids(self, active_student):
        creator = TaskUpdateNotificationCreator()
        n1 = creator.notify(active_student, "ctx1")
        n2 = creator.notify(active_student, "ctx2")
        assert n1.notification_id != n2.notification_id


# ════════════════════════════════════════════════════════════════════════════
# 3. ABSTRACT FACTORY TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestAbstractFactory:

    def test_local_file_store_save_and_retrieve(self):
        factory = LocalStorageFactory()
        fs = factory.create_file_store()
        uri = fs.save_file("doc.pdf", b"content")
        assert uri.startswith("local://")
        assert fs.get_file(uri) == b"content"

    def test_cloud_file_store_save_and_retrieve(self):
        factory = CloudStorageFactory()
        fs = factory.create_file_store()
        uri = fs.save_file("doc.pdf", b"cloud content")
        assert "cloud-storage.example.com" in uri

    def test_local_metadata_store_save_and_retrieve(self):
        factory = LocalStorageFactory()
        ms = factory.create_metadata_store()
        ms.save_metadata("doc-1", {"title": "Proposal"})
        result = ms.get_metadata("doc-1")
        assert result["title"] == "Proposal"

    def test_cloud_metadata_store_adds_cloud_flag(self):
        factory = CloudStorageFactory()
        ms = factory.create_metadata_store()
        ms.save_metadata("doc-1", {"title": "Cloud Doc"})
        result = ms.get_metadata("doc-1")
        assert result["_cloud"] is True

    def test_local_metadata_missing_key_raises(self):
        factory = LocalStorageFactory()
        ms = factory.create_metadata_store()
        with pytest.raises(KeyError):
            ms.get_metadata("nonexistent")

    def test_local_file_missing_uri_raises(self):
        factory = LocalStorageFactory()
        fs = factory.create_file_store()
        with pytest.raises(FileNotFoundError):
            fs.get_file("local://nowhere.pdf")

    def test_upload_document_helper_local(self):
        uri = upload_document(LocalStorageFactory(), "doc-x",
                              "paper.pdf", b"bytes")
        assert uri.startswith("local://")

    def test_upload_document_helper_cloud(self):
        uri = upload_document(CloudStorageFactory(), "doc-y",
                              "paper.pdf", b"bytes")
        assert "cloud-storage" in uri

    def test_factories_produce_independent_stores(self):
        fs1 = LocalStorageFactory().create_file_store()
        fs2 = LocalStorageFactory().create_file_store()
        fs1.save_file("a.pdf", b"aaa")
        with pytest.raises(FileNotFoundError):
            fs2.get_file("local://a.pdf")


# ════════════════════════════════════════════════════════════════════════════
# 4. BUILDER TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestBuilder:

    def test_minimal_project_build(self, active_supervisor):
        builder = ResearchProjectBuilder()
        director = ProjectDirector(builder)
        bp = director.build_minimal_project("p1", "AI Research", active_supervisor)
        assert bp.project is not None
        assert bp.project.title == "AI Research"

    def test_minimal_project_is_in_created_status(self, active_supervisor):
        builder = ResearchProjectBuilder()
        director = ProjectDirector(builder)
        bp = director.build_minimal_project("p1", "Draft", active_supervisor)
        assert bp.project.status == ProjectStatus.CREATED

    def test_active_project_status(self, active_supervisor, active_student):
        builder = ResearchProjectBuilder()
        director = ProjectDirector(builder)
        bp = director.build_active_project(
            "p2", "Cloud Research", "Desc",
            active_supervisor, [active_student],
            date.today() + timedelta(days=90),
        )
        assert bp.project.status == ProjectStatus.ACTIVE

    def test_active_project_has_members(self, active_supervisor, active_student):
        builder = ResearchProjectBuilder()
        director = ProjectDirector(builder)
        bp = director.build_active_project(
            "p3", "ML Study", "Desc",
            active_supervisor, [active_student],
            date.today() + timedelta(days=60),
        )
        members = bp.project.get_members()
        assert active_student in members

    def test_build_without_set_basic_info_raises(self):
        builder = ResearchProjectBuilder()
        with pytest.raises(ValueError, match="set_basic_info"):
            builder.build()

    def test_past_end_date_raises(self, active_supervisor):
        builder = ResearchProjectBuilder()
        builder.set_basic_info("p4", "Test", "desc", active_supervisor)
        with pytest.raises(ValueError, match="past"):
            builder.set_end_date(date.today() - timedelta(days=1))

    def test_builder_resets_after_build(self, active_supervisor):
        builder = ResearchProjectBuilder()
        builder.set_basic_info("p5", "Project A", "desc", active_supervisor)
        builder.build()
        # Builder should be reset — building again without set_basic_info should fail
        with pytest.raises(ValueError):
            builder.build()

    def test_fluent_chaining(self, active_supervisor):
        bp = (ResearchProjectBuilder()
              .set_basic_info("p6", "Chained", "desc", active_supervisor)
              .activate()
              .build())
        assert bp.project.status == ProjectStatus.ACTIVE


# ════════════════════════════════════════════════════════════════════════════
# 5. PROTOTYPE TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestPrototype:

    @pytest.fixture
    def cache(self, active_supervisor):
        return build_default_task_cache(active_supervisor)

    def test_cache_has_four_prototypes(self, cache):
        assert len(cache.list_prototypes()) == 4

    def test_clone_has_different_id(self, cache):
        clone = cache.get_clone("literature_review", "t-new")
        assert clone.task_id == "t-new"

    def test_clone_preserves_title(self, cache):
        clone = cache.get_clone("literature_review", "t-1")
        assert clone.title == "Literature Review"

    def test_clone_status_is_created(self, cache):
        clone = cache.get_clone("research_proposal", "t-2")
        assert clone.status == TaskStatus.CREATED

    def test_clone_assigned_to_is_none(self, cache):
        clone = cache.get_clone("progress_report", "t-3")
        assert clone.assigned_to is None

    def test_clone_deadline_override(self, cache):
        new_deadline = date.today() + timedelta(days=5)
        clone = cache.get_clone("final_submission", "t-4", new_deadline)
        assert clone.deadline == new_deadline

    def test_mutating_clone_does_not_affect_prototype(self, cache):
        clone = cache.get_clone("literature_review", "t-5")
        clone._title = "Mutated"
        original_clone = cache.get_clone("literature_review", "t-6")
        assert original_clone.title == "Literature Review"

    def test_two_clones_are_independent(self, cache):
        c1 = cache.get_clone("research_proposal", "t-7")
        c2 = cache.get_clone("research_proposal", "t-8")
        c1._title = "Clone 1 Only"
        assert c2.title == "Submit Research Proposal"

    def test_unknown_prototype_raises_key_error(self, cache):
        with pytest.raises(KeyError, match="unknown_task"):
            cache.get_clone("unknown_task", "t-x")

    def test_register_custom_prototype(self, cache, active_supervisor):
        custom = TaskPrototype(
            task_id="proto-custom",
            title="Ethics Approval",
            description="Obtain ethics committee approval.",
            deadline=date.today() + timedelta(days=30),
            created_by=active_supervisor,
        )
        cache.register("ethics_approval", custom)
        clone = cache.get_clone("ethics_approval", "t-eth")
        assert clone.title == "Ethics Approval"


# ════════════════════════════════════════════════════════════════════════════
# 6. SINGLETON TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestSingleton:

    def test_same_instance_returned_twice(self):
        db1 = DatabaseConnection.get_instance()
        db2 = DatabaseConnection.get_instance()
        assert db1 is db2

    def test_is_connected_on_creation(self):
        db = DatabaseConnection.get_instance()
        assert db.is_connected() is True

    def test_execute_logs_query(self):
        db = DatabaseConnection.get_instance()
        db.execute("SELECT 1")
        log = db.get_query_log()
        assert any("SELECT 1" in entry["query"] for entry in log)

    def test_execute_with_params(self):
        db = DatabaseConnection.get_instance()
        db.execute("SELECT * FROM users WHERE role = %(role)s",
                   {"role": "STUDENT"})
        log = db.get_query_log()
        assert log[-1]["params"] == {"role": "STUDENT"}

    def test_query_log_shared_across_references(self):
        db1 = DatabaseConnection.get_instance()
        db2 = DatabaseConnection.get_instance()
        db1.execute("SELECT 'shared'")
        assert db2.get_query_log() == db1.get_query_log()

    def test_execute_when_disconnected_raises(self):
        db = DatabaseConnection.get_instance()
        db.disconnect()
        with pytest.raises(ConnectionError):
            db.execute("SELECT 1")

    def test_thread_safety(self):
        """Multiple threads must receive the same singleton instance."""
        instances = []

        def get_instance():
            instances.append(DatabaseConnection.get_instance())

        threads = [threading.Thread(target=get_instance) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        first = instances[0]
        assert all(inst is first for inst in instances), \
            "Thread safety violated — multiple instances created"

    def test_reset_allows_new_instance(self):
        db1 = DatabaseConnection.get_instance()
        DatabaseConnection._reset_instance()
        db2 = DatabaseConnection.get_instance()
        assert db1 is not db2

    def test_repr_contains_host_and_db(self):
        db = DatabaseConnection.get_instance()
        r = repr(db)
        assert "localhost" in r
        assert "research_platform" in r
