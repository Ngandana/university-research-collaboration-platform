"""
test_src_classes.py
Unit tests for core domain classes (src/).
Tests attributes, methods, relationships, and business rule enforcement.
"""

import sys
import os
from datetime import date, timedelta
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.user import User, UserRole, UserStatus
from src.research_project import ResearchProject, ProjectStatus
from src.document import Document, DocumentStatus, DocumentVersion
from src.task import Task, TaskStatus
from src.communication import (Message, MessageStatus, Notification,
                                NotificationType, Invitation, InvitationStatus)
from creational_patterns.simple_factory import UserFactory


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def supervisor():
    u = UserFactory.create_user("s1", "Prof Nkosi", "n@uni.ac.za",
                                "pw", "supervisor")
    u.register()
    return u


@pytest.fixture
def student():
    u = UserFactory.create_user("st1", "Alice", "a@uni.ac.za",
                                "pw", "student")
    u.register()
    return u


@pytest.fixture
def project(supervisor):
    p = ResearchProject("p1", "AI Research", "Exploring AI", supervisor)
    p.activate()
    return p


# ── User Tests ────────────────────────────────────────────────────────────────

class TestUser:

    def test_register_transitions_to_active(self):
        u = UserFactory.create_user("u1", "T", "t@u.ac.za", "pw", "student")
        assert u.status == UserStatus.REGISTERED
        u.register()
        assert u.status == UserStatus.ACTIVE

    def test_suspend_active_user(self, student):
        student.suspend()
        assert student.status == UserStatus.SUSPENDED

    def test_reactivate_suspended_user(self, student):
        student.suspend()
        student.reactivate()
        assert student.status == UserStatus.ACTIVE

    def test_deactivate_user(self, student):
        student.deactivate()
        assert student.status == UserStatus.DEACTIVATED

    def test_update_profile_changes_name(self, student):
        student.update_profile(name="Alice Updated")
        assert student.name == "Alice Updated"

    def test_update_profile_inactive_raises(self):
        u = UserFactory.create_user("u2", "T", "t@u.ac.za", "pw", "student")
        with pytest.raises(PermissionError):
            u.update_profile(name="New Name")

    def test_login_before_activate_fails(self):
        u = UserFactory.create_user("u3", "T", "t@u.ac.za", "mypass", "student")
        assert u.login("mypass") is False


# ── ResearchProject Tests ─────────────────────────────────────────────────────

class TestResearchProject:

    def test_initial_status_created(self, supervisor):
        p = ResearchProject("p2", "Test", "desc", supervisor)
        assert p.status == ProjectStatus.CREATED

    def test_activate(self, supervisor):
        p = ResearchProject("p2", "Test", "desc", supervisor)
        p.activate()
        assert p.status == ProjectStatus.ACTIVE

    def test_complete(self, project):
        project.complete()
        assert project.status == ProjectStatus.COMPLETED

    def test_cancel(self, project):
        project.cancel()
        assert project.status == ProjectStatus.CANCELLED

    def test_archive_after_complete(self, project):
        project.complete()
        project.archive()
        assert project.status == ProjectStatus.ARCHIVED

    def test_add_member(self, project, student):
        project.add_member(student)
        assert student in project.get_members()

    def test_remove_member(self, project, student):
        project.add_member(student)
        project.remove_member(student)
        assert student not in project.get_members()

    def test_cannot_remove_owner(self, project, supervisor):
        project.remove_member(supervisor)
        assert supervisor in project.get_members()

    def test_add_member_to_archived_raises(self, project, student):
        project.complete()
        project.archive()
        with pytest.raises(PermissionError):
            project.add_member(student)


# ── Document Tests ────────────────────────────────────────────────────────────

class TestDocument:

    def test_valid_pdf_upload(self, student):
        doc = Document("d1", "Proposal", student)
        doc.upload("proposal.pdf", "pdf", 2.0, "v1")
        assert doc.status == DocumentStatus.STORED
        assert len(doc.get_version_history()) == 1

    def test_invalid_file_type_rejected(self, student):
        doc = Document("d2", "Malware", student)
        doc.upload("bad.exe", "exe", 1.0, "v1")
        assert doc.status == DocumentStatus.REJECTED
        assert len(doc.get_version_history()) == 0

    def test_oversized_file_rejected(self, student):
        doc = Document("d3", "Huge", student)
        doc.upload("huge.pdf", "pdf", 999.0, "v1")
        assert doc.status == DocumentStatus.REJECTED

    def test_update_adds_version(self, student):
        doc = Document("d4", "Draft", student)
        doc.upload("draft.pdf", "pdf", 1.0, "v1")
        doc.update("final.pdf", "pdf", 1.5, "v2")
        assert len(doc.get_version_history()) == 2

    def test_version_numbers_increment(self, student):
        doc = Document("d5", "Paper", student)
        doc.upload("v1.pdf", "pdf", 1.0, "ver1")
        doc.update("v2.pdf", "pdf", 1.0, "ver2")
        versions = doc.get_version_history()
        assert versions[0].version_number == 1
        assert versions[1].version_number == 2

    def test_docx_is_allowed(self, student):
        doc = Document("d6", "Report", student)
        doc.upload("report.docx", "docx", 3.0, "v1")
        assert doc.status == DocumentStatus.STORED


# ── Task Tests ────────────────────────────────────────────────────────────────

class TestTask:

    def test_assign_transitions_status(self, supervisor, student):
        t = Task("t1", "Literature Review", "Read papers",
                 date.today() + timedelta(days=14), supervisor)
        t.assign(student)
        assert t.status == TaskStatus.ASSIGNED
        assert t.assigned_to is student

    def test_start_task(self, supervisor, student):
        t = Task("t2", "Proposal", "Write",
                 date.today() + timedelta(days=7), supervisor)
        t.assign(student)
        t.start()
        assert t.status == TaskStatus.IN_PROGRESS

    def test_complete_task(self, supervisor, student):
        t = Task("t3", "Submit", "Upload",
                 date.today() + timedelta(days=3), supervisor)
        t.assign(student)
        t.start()
        t.complete()
        assert t.status == TaskStatus.COMPLETED

    def test_mark_overdue(self, supervisor, student):
        past_deadline = date.today() - timedelta(days=1)
        t = Task("t4", "Late Task", "Overdue",
                 past_deadline, supervisor)
        t.assign(student)
        t.mark_overdue()
        assert t.status == TaskStatus.OVERDUE

    def test_overdue_can_still_complete(self, supervisor, student):
        past = date.today() - timedelta(days=1)
        t = Task("t5", "Late", "Late", past, supervisor)
        t.assign(student)
        t.mark_overdue()
        t.complete()
        assert t.status == TaskStatus.COMPLETED

    def test_cannot_assign_completed_task(self, supervisor, student):
        t = Task("t6", "Done", "done", date.today(), supervisor)
        t.assign(student)
        t.start()
        t.complete()
        with pytest.raises(ValueError):
            t.assign(student)


# ── Message & Notification Tests ──────────────────────────────────────────────

class TestCommunication:

    def test_message_send_transitions_status(self, supervisor, student):
        msg = Message("m1", "Hello!", supervisor, student)
        msg.send()
        assert msg.status == MessageStatus.SENT

    def test_message_deliver_creates_notification(self, supervisor, student):
        msg = Message("m2", "Review needed", supervisor, student)
        msg.send()
        notif = msg.deliver()
        assert notif is not None
        assert notif.notification_type == NotificationType.MESSAGE_RECEIVED

    def test_message_mark_read(self, supervisor, student):
        msg = Message("m3", "Hi", supervisor, student)
        msg.send()
        msg.deliver()
        msg.mark_read()
        assert msg.status == MessageStatus.READ

    def test_empty_message_raises(self, supervisor, student):
        with pytest.raises(ValueError):
            Message("m4", "   ", supervisor, student)

    def test_invitation_accept_adds_member(self, supervisor, student, project):
        inv = Invitation("i1", supervisor, student, project)
        inv.accept()
        assert inv.status == InvitationStatus.ACCEPTED
        assert student in project.get_members()

    def test_invitation_reject(self, supervisor, student, project):
        inv = Invitation("i2", supervisor, student, project)
        inv.reject()
        assert inv.status == InvitationStatus.REJECTED

    def test_invitation_expire(self, supervisor, student, project):
        inv = Invitation("i3", supervisor, student, project)
        inv.expire()
        assert inv.status == InvitationStatus.EXPIRED
