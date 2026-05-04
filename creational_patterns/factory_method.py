"""
factory_method.py
Pattern: Factory Method
──────────────────────────────────────────────────────────────────────────────
Use case: Notification creation delegated to concrete subclasses.

Different system events (task updates, message receipt, project updates) need
to produce Notifications with different content and type.  A NotificationCreator
abstract base class defines the factory method; concrete subclasses decide
exactly how to build each Notification.

This maps to FR9 (Notifications) — the notification system must handle
multiple trigger types without the caller knowing construction details.
"""

from abc import ABC, abstractmethod
import uuid
from src.communication import Notification, NotificationType
from src.user import User


# ── Abstract Creator ──────────────────────────────────────────────────────────

class NotificationCreator(ABC):
    """
    Abstract creator declaring the factory method.
    Subclasses override `create_notification` to produce the right type.
    """

    @abstractmethod
    def create_notification(self, recipient: User,
                            context: str) -> Notification:
        """Factory method — subclasses provide the concrete Notification."""
        ...

    def notify(self, recipient: User, context: str) -> Notification:
        """
        Template method: create and deliver a notification.
        The factory method is called here; construction is delegated to subclass.
        """
        notification = self.create_notification(recipient, context)
        # In a real system this would push to a queue / email service
        return notification


# ── Concrete Creators ─────────────────────────────────────────────────────────

class TaskUpdateNotificationCreator(NotificationCreator):
    """Creates notifications for task status changes (FR7, FR8)."""

    def create_notification(self, recipient: User,
                            context: str) -> Notification:
        return Notification(
            notification_id=f"notif-task-{uuid.uuid4().hex[:8]}",
            message=f"Task update: {context}",
            notification_type=NotificationType.TASK_UPDATE,
            recipient=recipient,
        )


class MessageReceivedNotificationCreator(NotificationCreator):
    """Creates notifications when a new message arrives (FR9)."""

    def create_notification(self, recipient: User,
                            context: str) -> Notification:
        return Notification(
            notification_id=f"notif-msg-{uuid.uuid4().hex[:8]}",
            message=f"New message from {context}",
            notification_type=NotificationType.MESSAGE_RECEIVED,
            recipient=recipient,
        )


class ProjectUpdateNotificationCreator(NotificationCreator):
    """Creates notifications for project lifecycle changes (FR3)."""

    def create_notification(self, recipient: User,
                            context: str) -> Notification:
        return Notification(
            notification_id=f"notif-proj-{uuid.uuid4().hex[:8]}",
            message=f"Project update: {context}",
            notification_type=NotificationType.PROJECT_UPDATE,
            recipient=recipient,
        )


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from src.user import UserRole, UserStatus
    from creational_patterns.simple_factory import UserFactory

    student = UserFactory.create_user("u1", "Alice", "alice@uni.ac.za",
                                      "pw", "student")
    student.register()

    task_creator = TaskUpdateNotificationCreator()
    notif = task_creator.notify(student, "Literature Review marked Overdue")
    print(notif)

    msg_creator = MessageReceivedNotificationCreator()
    notif2 = msg_creator.notify(student, "Prof Nkosi")
    print(notif2)
