"""
abstract_factory.py
Pattern: Abstract Factory
──────────────────────────────────────────────────────────────────────────────
Use case: Storage service families — local vs. cloud.

The platform stores Documents either locally (dev/test) or in cloud storage
(production).  An abstract factory produces a matching set of related objects:
a FileStore (handles raw file bytes) and a MetadataStore (handles document
records).  Switching environments only requires swapping the factory; no
call-site code changes.

This maps to the Container Diagram (Assignment 3) where Cloud Storage is a
distinct container, and to FR5 (Document Upload).
"""

from abc import ABC, abstractmethod
from typing import Dict


# ── Abstract Products ─────────────────────────────────────────────────────────

class FileStore(ABC):
    """Abstract product — handles raw file persistence."""

    @abstractmethod
    def save_file(self, path: str, content: bytes) -> str:
        """Save file bytes; return storage URI."""
        ...

    @abstractmethod
    def get_file(self, uri: str) -> bytes:
        """Retrieve file bytes by URI."""
        ...


class MetadataStore(ABC):
    """Abstract product — handles document metadata persistence."""

    @abstractmethod
    def save_metadata(self, doc_id: str, metadata: Dict) -> None:
        """Persist document metadata."""
        ...

    @abstractmethod
    def get_metadata(self, doc_id: str) -> Dict:
        """Retrieve document metadata."""
        ...


# ── Concrete Products — Local ─────────────────────────────────────────────────

class LocalFileStore(FileStore):
    """Stores files in memory (simulating local disk for dev/test)."""

    def __init__(self):
        self._store: Dict[str, bytes] = {}

    def save_file(self, path: str, content: bytes) -> str:
        self._store[path] = content
        return f"local://{path}"

    def get_file(self, uri: str) -> bytes:
        path = uri.replace("local://", "")
        if path not in self._store:
            raise FileNotFoundError(f"No local file at {uri}")
        return self._store[path]


class LocalMetadataStore(MetadataStore):
    """Stores metadata in a plain dict (simulating SQLite for dev/test)."""

    def __init__(self):
        self._store: Dict[str, Dict] = {}

    def save_metadata(self, doc_id: str, metadata: Dict) -> None:
        self._store[doc_id] = metadata

    def get_metadata(self, doc_id: str) -> Dict:
        if doc_id not in self._store:
            raise KeyError(f"No metadata for document {doc_id}")
        return self._store[doc_id]


# ── Concrete Products — Cloud ─────────────────────────────────────────────────

class CloudFileStore(FileStore):
    """Simulates cloud object storage (e.g. Huawei OBS / AWS S3)."""

    def __init__(self):
        self._store: Dict[str, bytes] = {}

    def save_file(self, path: str, content: bytes) -> str:
        self._store[path] = content
        return f"https://cloud-storage.example.com/{path}"

    def get_file(self, uri: str) -> bytes:
        key = uri.split("/")[-1]
        if key not in self._store and uri not in self._store:
            raise FileNotFoundError(f"No cloud object at {uri}")
        return self._store.get(uri, self._store.get(key, b""))


class CloudMetadataStore(MetadataStore):
    """Simulates a managed cloud database (e.g. Huawei RDS / PostgreSQL)."""

    def __init__(self):
        self._store: Dict[str, Dict] = {}

    def save_metadata(self, doc_id: str, metadata: Dict) -> None:
        self._store[doc_id] = {**metadata, "_cloud": True}

    def get_metadata(self, doc_id: str) -> Dict:
        if doc_id not in self._store:
            raise KeyError(f"No cloud metadata for document {doc_id}")
        return self._store[doc_id]


# ── Abstract Factory ──────────────────────────────────────────────────────────

class StorageFactory(ABC):
    """Abstract factory — creates a matched FileStore + MetadataStore pair."""

    @abstractmethod
    def create_file_store(self) -> FileStore:
        ...

    @abstractmethod
    def create_metadata_store(self) -> MetadataStore:
        ...


# ── Concrete Factories ────────────────────────────────────────────────────────

class LocalStorageFactory(StorageFactory):
    """Produces local storage objects (used in development / testing)."""

    def create_file_store(self) -> FileStore:
        return LocalFileStore()

    def create_metadata_store(self) -> MetadataStore:
        return LocalMetadataStore()


class CloudStorageFactory(StorageFactory):
    """Produces cloud storage objects (used in production)."""

    def create_file_store(self) -> FileStore:
        return CloudFileStore()

    def create_metadata_store(self) -> MetadataStore:
        return CloudMetadataStore()


# ── Client helper ─────────────────────────────────────────────────────────────

def upload_document(factory: StorageFactory, doc_id: str,
                    file_path: str, content: bytes) -> str:
    """
    Client code — works with any StorageFactory without knowing concrete types.
    """
    file_store = factory.create_file_store()
    meta_store = factory.create_metadata_store()

    uri = file_store.save_file(file_path, content)
    meta_store.save_metadata(doc_id, {"uri": uri, "path": file_path})
    return uri


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    content = b"%PDF-1.4 sample content"

    local_uri = upload_document(LocalStorageFactory(), "doc-1",
                                "proposal.pdf", content)
    print(f"Local:  {local_uri}")

    cloud_uri = upload_document(CloudStorageFactory(), "doc-1",
                                "proposal.pdf", content)
    print(f"Cloud:  {cloud_uri}")
