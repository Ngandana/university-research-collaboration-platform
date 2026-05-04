"""
document.py
Document and DocumentVersion entities.
Document composes DocumentVersions (each upload creates a new version).
"""

from enum import Enum
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from user import User

ALLOWED_FILE_TYPES = {"pdf", "docx"}
MAX_FILE_SIZE_MB = 50


class DocumentStatus(Enum):
    UPLOADED = "UPLOADED"
    VALIDATED = "VALIDATED"
    STORED = "STORED"
    REJECTED = "REJECTED"
    UPDATED = "UPDATED"


class DocumentVersion:
    """
    Represents a single version of a document.
    Created each time a Document is uploaded or updated.
    """

    def __init__(self, version_id: str, version_number: int,
                 file_path: str, uploaded_by: "User"):
        self._version_id = version_id
        self._version_number = version_number
        self._file_path = file_path
        self._uploaded_by = uploaded_by
        self._uploaded_date = datetime.now()

    @property
    def version_id(self) -> str:
        return self._version_id

    @property
    def version_number(self) -> int:
        return self._version_number

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def uploaded_by(self) -> "User":
        return self._uploaded_by

    @property
    def uploaded_date(self) -> datetime:
        return self._uploaded_date

    def save(self) -> None:
        """Persist version record (stub — handled by storage service)."""
        pass

    def retrieve(self) -> str:
        """Return path to versioned file."""
        return self._file_path

    def get_version_number(self) -> int:
        return self._version_number

    def __repr__(self) -> str:
        return (f"DocumentVersion(v{self._version_number}, "
                f"path={self._file_path})")


class Document:
    """
    Represents a research document within a project.
    Composed of DocumentVersion records; each update adds a new version.
    Business rules:
      - Only PDF and DOCX file types are accepted.
      - File size must not exceed MAX_FILE_SIZE_MB.
    """

    def __init__(self, document_id: str, title: str, uploaded_by: "User"):
        self._document_id = document_id
        self._title = title
        self._uploaded_by = uploaded_by
        self._file_type: str = ""
        self._file_size: float = 0.0  # MB
        self._status = DocumentStatus.UPLOADED
        self._uploaded_date = datetime.now()
        self._versions: List[DocumentVersion] = []
        self._rejection_reason: str = ""

    # ── Getters ───────────────────────────────────────────────────────────────
    @property
    def document_id(self) -> str:
        return self._document_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def status(self) -> DocumentStatus:
        return self._status

    @property
    def file_type(self) -> str:
        return self._file_type

    @property
    def file_size(self) -> float:
        return self._file_size

    # ── Lifecycle methods ─────────────────────────────────────────────────────
    def upload(self, file_path: str, file_type: str, file_size_mb: float,
               version_id: str) -> None:
        """Initiate an upload; sets metadata and transitions to UPLOADED."""
        self._file_type = file_type.lower()
        self._file_size = file_size_mb
        self._status = DocumentStatus.UPLOADED
        # Validate immediately after upload
        if self.validate():
            new_version = DocumentVersion(
                version_id=version_id,
                version_number=len(self._versions) + 1,
                file_path=file_path,
                uploaded_by=self._uploaded_by,
            )
            self._versions.append(new_version)
            self.store()

    def validate(self) -> bool:
        """Check file type and size; reject if invalid."""
        if self._file_type not in ALLOWED_FILE_TYPES:
            self.reject(f"Unsupported file type: {self._file_type}")
            return False
        if self._file_size > MAX_FILE_SIZE_MB:
            self.reject(f"File size {self._file_size}MB exceeds "
                        f"{MAX_FILE_SIZE_MB}MB limit.")
            return False
        self._status = DocumentStatus.VALIDATED
        return True

    def store(self) -> None:
        """Mark document as stored after successful validation."""
        if self._status == DocumentStatus.VALIDATED:
            self._status = DocumentStatus.STORED

    def reject(self, reason: str) -> None:
        """Mark document as rejected with a reason."""
        self._status = DocumentStatus.REJECTED
        self._rejection_reason = reason

    def update(self, file_path: str, file_type: str, file_size_mb: float,
               version_id: str) -> None:
        """Upload a new version; adds to version history."""
        self._status = DocumentStatus.UPDATED
        self.upload(file_path, file_type, file_size_mb, version_id)

    def get_version_history(self) -> List[DocumentVersion]:
        return list(self._versions)

    def get_status(self) -> DocumentStatus:
        return self._status

    def __repr__(self) -> str:
        return (f"Document(id={self._document_id}, title={self._title}, "
                f"status={self._status.value}, versions={len(self._versions)})")
