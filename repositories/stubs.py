"""
repositories/stubs.py
Future-Proofing — Stub implementations for non-memory storage backends.

These stubs fulfil the interface contract so the RepositoryFactory can
reference them without errors, while making it clear to future developers
exactly what needs to be implemented to activate each backend.

Each stub raises NotImplementedError on any call, with a descriptive message
pointing to what library/approach to use for the real implementation.

Planned backends:
  FileSystem — serialize entities to JSON files (json / pathlib).
  Database   — persist to PostgreSQL via psycopg2 or SQLAlchemy ORM.
"""

import json
import os
from typing import Optional, List, Dict
from pathlib import Path

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from repositories.interfaces import (
    UserRepository, ResearchProjectRepository,
)


# ═════════════════════════════════════════════════════════════════════════════
# FILESYSTEM STUBS
# Full implementation: use json.dump / json.load with pathlib.Path.
# Each entity maps to a single JSON file, keyed by entity ID.
# ═════════════════════════════════════════════════════════════════════════════

class FileSystemUserRepository(UserRepository):
    """
    Stub — will persist User objects as JSON in a flat file.

    Full implementation plan:
      - __init__(self, file_path: str): load existing JSON on startup.
      - save(): json.dump entire dict to file after update.
      - find_by_id(): return deserialized User object by key.
      - delete(): remove key and re-dump.
      - Serialization: implement User.to_dict() / User.from_dict(data).

    Example file format:
      {
        "u-001": {"user_id": "u-001", "name": "Alice", "role": "STUDENT", ...},
        "u-002": { ... }
      }
    """

    def __init__(self, file_path: str = "data/users.json"):
        self._file_path = Path(file_path)
        # TODO: self._file_path.parent.mkdir(parents=True, exist_ok=True)
        # TODO: self._storage = self._load()

    def _load(self) -> Dict:
        if self._file_path.exists():
            with open(self._file_path, "r") as f:
                return json.load(f)
        return {}

    def _flush(self, data: Dict) -> None:
        with open(self._file_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    # All methods raise until implemented
    def save(self, entity) -> None:
        raise NotImplementedError(
            "FileSystemUserRepository.save() not yet implemented. "
            "Implement User.to_dict() then call self._flush()."
        )

    def find_by_id(self, entity_id: str) -> Optional[object]:
        raise NotImplementedError(
            "FileSystemUserRepository.find_by_id() not yet implemented. "
            "Call self._load() and deserialize with User.from_dict()."
        )

    def find_all(self) -> List:
        raise NotImplementedError("Not yet implemented.")

    def delete(self, entity_id: str) -> None:
        raise NotImplementedError("Not yet implemented.")

    def exists(self, entity_id: str) -> bool:
        raise NotImplementedError("Not yet implemented.")

    def count(self) -> int:
        raise NotImplementedError("Not yet implemented.")

    def find_by_email(self, email: str):
        raise NotImplementedError("Not yet implemented.")

    def find_by_role(self, role) -> List:
        raise NotImplementedError("Not yet implemented.")

    def find_by_status(self, status) -> List:
        raise NotImplementedError("Not yet implemented.")


class FileSystemResearchProjectRepository(ResearchProjectRepository):
    """
    Stub — will persist ResearchProject objects as JSON.

    Full implementation plan:
      - Same pattern as FileSystemUserRepository.
      - ResearchProject.to_dict() must serialize members as a list of user_ids.
      - Reconstruction requires a UserRepository to resolve member references.
    """

    def __init__(self, file_path: str = "data/projects.json"):
        self._file_path = Path(file_path)

    def save(self, entity) -> None:
        raise NotImplementedError(
            "FileSystemResearchProjectRepository.save() not yet implemented."
        )

    def find_by_id(self, entity_id: str) -> Optional[object]:
        raise NotImplementedError("Not yet implemented.")

    def find_all(self) -> List:
        raise NotImplementedError("Not yet implemented.")

    def delete(self, entity_id: str) -> None:
        raise NotImplementedError("Not yet implemented.")

    def exists(self, entity_id: str) -> bool:
        raise NotImplementedError("Not yet implemented.")

    def count(self) -> int:
        raise NotImplementedError("Not yet implemented.")

    def find_by_owner(self, owner_id: str) -> List:
        raise NotImplementedError("Not yet implemented.")

    def find_by_status(self, status) -> List:
        raise NotImplementedError("Not yet implemented.")

    def find_by_member(self, user_id: str) -> List:
        raise NotImplementedError("Not yet implemented.")


# ═════════════════════════════════════════════════════════════════════════════
# DATABASE STUBS
# Full implementation: use psycopg2 (raw SQL) or SQLAlchemy ORM.
# Connection settings loaded from environment variables (DATABASE_URL).
# ═════════════════════════════════════════════════════════════════════════════

class DatabaseUserRepository(UserRepository):
    """
    Stub — will persist User objects to PostgreSQL.

    Full implementation plan:
      - __init__(): obtain connection from DatabaseConnection singleton
        (already implemented in creational_patterns/singleton.py).
      - save(): INSERT INTO users ... ON CONFLICT (user_id) DO UPDATE ...
      - find_by_id(): SELECT * FROM users WHERE user_id = %s
      - find_all(): SELECT * FROM users
      - delete(): DELETE FROM users WHERE user_id = %s
      - find_by_email(): SELECT * FROM users WHERE email = %s

    Schema:
      CREATE TABLE users (
          user_id     VARCHAR PRIMARY KEY,
          name        VARCHAR NOT NULL,
          email       VARCHAR UNIQUE NOT NULL,
          password_hash VARCHAR NOT NULL,
          role        VARCHAR NOT NULL,
          status      VARCHAR NOT NULL,
          created_date DATE NOT NULL
      );
    """

    def __init__(self):
        # TODO: from creational_patterns.singleton import DatabaseConnection
        # TODO: self._db = DatabaseConnection.get_instance()
        pass

    def save(self, entity) -> None:
        raise NotImplementedError(
            "DatabaseUserRepository.save() not yet implemented. "
            "Use: INSERT INTO users ... ON CONFLICT DO UPDATE ..."
        )

    def find_by_id(self, entity_id: str) -> Optional[object]:
        raise NotImplementedError(
            "DatabaseUserRepository.find_by_id() not yet implemented. "
            "Use: SELECT * FROM users WHERE user_id = %s"
        )

    def find_all(self) -> List:
        raise NotImplementedError("Not yet implemented.")

    def delete(self, entity_id: str) -> None:
        raise NotImplementedError("Not yet implemented.")

    def exists(self, entity_id: str) -> bool:
        raise NotImplementedError("Not yet implemented.")

    def count(self) -> int:
        raise NotImplementedError("Not yet implemented.")

    def find_by_email(self, email: str):
        raise NotImplementedError("Not yet implemented.")

    def find_by_role(self, role) -> List:
        raise NotImplementedError("Not yet implemented.")

    def find_by_status(self, status) -> List:
        raise NotImplementedError("Not yet implemented.")


class DatabaseResearchProjectRepository(ResearchProjectRepository):
    """
    Stub — will persist ResearchProject objects to PostgreSQL.

    Schema:
      CREATE TABLE research_projects (
          project_id   VARCHAR PRIMARY KEY,
          title        VARCHAR NOT NULL,
          description  TEXT,
          owner_id     VARCHAR REFERENCES users(user_id),
          status       VARCHAR NOT NULL,
          created_date DATE NOT NULL,
          end_date     DATE
      );
      CREATE TABLE project_members (
          project_id VARCHAR REFERENCES research_projects(project_id),
          user_id    VARCHAR REFERENCES users(user_id),
          PRIMARY KEY (project_id, user_id)
      );
    """

    def __init__(self):
        pass  # TODO: inject DatabaseConnection

    def save(self, entity) -> None:
        raise NotImplementedError(
            "DatabaseResearchProjectRepository.save() not yet implemented."
        )

    def find_by_id(self, entity_id: str) -> Optional[object]:
        raise NotImplementedError("Not yet implemented.")

    def find_all(self) -> List:
        raise NotImplementedError("Not yet implemented.")

    def delete(self, entity_id: str) -> None:
        raise NotImplementedError("Not yet implemented.")

    def exists(self, entity_id: str) -> bool:
        raise NotImplementedError("Not yet implemented.")

    def count(self) -> int:
        raise NotImplementedError("Not yet implemented.")

    def find_by_owner(self, owner_id: str) -> List:
        raise NotImplementedError("Not yet implemented.")

    def find_by_status(self, status) -> List:
        raise NotImplementedError("Not yet implemented.")

    def find_by_member(self, user_id: str) -> List:
        raise NotImplementedError("Not yet implemented.")
