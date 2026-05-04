"""
communication.py
Message, Notification, and Invitation entities.
"""

from enum import Enum
from datetime import datetime, date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from user import User
    from research_project import ResearchProject


# ── Enumerations ──────────────────────────────────────────────────────────────

class MessageStatus(Enum):
    COMPOSED = "COMPOSED"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    READ = "READ"


class NotificationType(Enum):
    TASK_UPDATE = "TASK_UPDATE"
    MESSAGE_RECEIVED = "MESSAGE_RECEIVED"
    PROJECT_UPDATE = "PROJECT_UPDATE"


class InvitationStatus(Enum):
    SENT = "SENT"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


# ── Message ───────────────────────────────────────────────────────────────────

class Message:
    """
    Represents a message sent between platform users.
    Triggers a Notification upon successful delivery.
    """

    def __init__(self, message_id: str, content: str,
                 sender: "User", recipient: "User"):
        if not content or not content.strip():
            raise ValueError("Message content cannot be empty.")
        self._message_id = message_id
        self._content = content
        self._sender = sender
        self._recipient = recipient
        self._status = MessageStatus.COMPOSED
        self._sent_date: datetime = None
        self._notification: "Notification" = None

    @property
    def message_id(self) -> str:
        return self._message_id

    @property
    def content(self) -> str:
        return self._content

    @property
    def sender(self) -> "User":
        return self._sender

    @property
    def recipient(self) -> "User":
        return self._recipient

    @property
    def status(self) -> MessageStatus:
        return self._status

    @property
    def notification(self) -> "Notification":
        return self._notification

    def send(self) -> None:
        """Transition from COMPOSED to SENT."""
        if self._status == MessageStatus.COMPOSED:
            self._status = MessageStatus.SENT
            self._sent_date = datetime.now()

    def deliver(self) -> "Notification":
        """Transition to DELIVERED and trigger a Notification."""
        if self._status == MessageStatus.SENT:
            self._status = MessageStatus.DELIVERED
            self._notification = Notification(
                notification_id=f"notif-{self._message_id}",
                message=f"New message from {self._sender.name}",
                notification_type=NotificationType.MESSAGE_RECEIVED,
                recipient=self._recipient,
            )
        return self._notification

    def mark_read(self) -> None:
        if self._status == MessageStatus.DELIVERED:
            self._status = MessageStatus.READ

    def get_status(self) -> MessageStatus:
        return self._status

    def __repr__(self) -> str:
        return (f"Message(id={self._message_id}, "
                f"from={self._sender.name}, status={self._status.value})")


# ── Notification ──────────────────────────────────────────────────────────────

class Notification:
    """
    Represents an in-platform notification delivered to a user.
    Created automatically when a Message is delivered or a Task changes state.
    """

    def __init__(self, notification_id: str, message: str,
                 notification_type: NotificationType, recipient: "User"):
        self._notification_id = notification_id
        self._message = message
        self._type = notification_type
        self._recipient = recipient
        self._is_read = False
        self._created_date = datetime.now()

    @property
    def notification_id(self) -> str:
        return self._notification_id

    @property
    def message(self) -> str:
        return self._message

    @property
    def notification_type(self) -> NotificationType:
        return self._type

    @property
    def recipient(self) -> "User":
        return self._recipient

    @property
    def is_read(self) -> bool:
        return self._is_read

    @property
    def created_date(self) -> datetime:
        return self._created_date

    def mark_read(self) -> None:
        self._is_read = True

    def dismiss(self) -> None:
        self._is_read = True

    def __repr__(self) -> str:
        return (f"Notification(id={self._notification_id}, "
                f"type={self._type.value}, read={self._is_read})")


# ── Invitation ────────────────────────────────────────────────────────────────

class Invitation:
    """
    Represents a project membership invitation from a Supervisor to a User.
    Gate for joining a ResearchProject (FR4 / UC7).
    """

    def __init__(self, invitation_id: str, sender: "User",
                 recipient: "User", project: "ResearchProject"):
        self._invitation_id = invitation_id
        self._sender = sender
        self._recipient = recipient
        self._project = project
        self._status = InvitationStatus.SENT
        self._sent_date = date.today()

    @property
    def invitation_id(self) -> str:
        return self._invitation_id

    @property
    def sender(self) -> "User":
        return self._sender

    @property
    def recipient(self) -> "User":
        return self._recipient

    @property
    def project(self) -> "ResearchProject":
        return self._project

    @property
    def status(self) -> InvitationStatus:
        return self._status

    def send(self) -> None:
        """Re-send or confirm dispatch."""
        self._status = InvitationStatus.SENT

    def accept(self) -> None:
        """Recipient accepts — add them to the project."""
        if self._status == InvitationStatus.SENT:
            self._status = InvitationStatus.ACCEPTED
            self._project.add_member(self._recipient)

    def reject(self) -> None:
        if self._status == InvitationStatus.SENT:
            self._status = InvitationStatus.REJECTED

    def expire(self) -> None:
        if self._status == InvitationStatus.SENT:
            self._status = InvitationStatus.EXPIRED

    def get_status(self) -> InvitationStatus:
        return self._status

    def __repr__(self) -> str:
        return (f"Invitation(id={self._invitation_id}, "
                f"to={self._recipient.name}, status={self._status.value})")
