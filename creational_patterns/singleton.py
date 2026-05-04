"""
singleton.py
Pattern: Singleton
──────────────────────────────────────────────────────────────────────────────
Use case: DatabaseConnection — exactly one active connection pool.

The platform's Backend API must share a single connection pool to the
PostgreSQL database (identified in the Container Diagram, Assignment 3).
Creating multiple pools wastes resources and can exhaust database connections.
The Singleton ensures that regardless of how many parts of the application
request a connection, only one DatabaseConnection instance exists.

Thread safety is achieved via a threading.Lock, satisfying the NFR for
scalability under concurrent load (Assignment 4 NFR — Scalability).
"""

import threading
import uuid
from typing import Optional, Dict, Any


class DatabaseConnection:
    """
    Thread-safe Singleton representing the application's database connection pool.

    Usage:
        db = DatabaseConnection.get_instance()
        db.execute("SELECT * FROM users")

    Guarantees:
        - Only one instance exists per process.
        - Concurrent threads receive the same instance.
        - Connection is established only once (lazy initialisation).
    """

    _instance: Optional["DatabaseConnection"] = None
    _lock: threading.Lock = threading.Lock()

    def __init__(self, host: str = "localhost", port: int = 5432,
                 database: str = "research_platform", user: str = "app_user"):
        # Guard: prevent direct instantiation after singleton is created
        if DatabaseConnection._instance is not None:
            raise RuntimeError(
                "DatabaseConnection is a singleton. "
                "Use DatabaseConnection.get_instance() instead."
            )
        self._host = host
        self._port = port
        self._database = database
        self._user = user
        self._connected = False
        self._query_log: list = []
        self._connect()

    # ── Singleton accessor ────────────────────────────────────────────────────

    @classmethod
    def get_instance(cls, host: str = "localhost", port: int = 5432,
                     database: str = "research_platform",
                     user: str = "app_user") -> "DatabaseConnection":
        """
        Return the single DatabaseConnection instance.
        Creates it on first call (lazy initialisation).
        Thread-safe via double-checked locking.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls.__new__(cls)
                    # Manually call __init__ since we bypassed the constructor
                    cls._instance._host = host
                    cls._instance._port = port
                    cls._instance._database = database
                    cls._instance._user = user
                    cls._instance._connected = False
                    cls._instance._query_log = []
                    cls._instance._connect()
        return cls._instance

    # ── Connection lifecycle ──────────────────────────────────────────────────

    def _connect(self) -> None:
        """Simulate establishing a database connection."""
        # In production: psycopg2.connect(...) or SQLAlchemy engine
        self._connected = True

    def disconnect(self) -> None:
        """Close the connection (used on app shutdown)."""
        self._connected = False

    def is_connected(self) -> bool:
        return self._connected

    # ── Query interface ───────────────────────────────────────────────────────

    def execute(self, query: str, params: Dict[str, Any] = None) -> Dict:
        """
        Execute a SQL query.
        Logs every query for audit purposes.
        Returns a stub result dict.
        """
        if not self._connected:
            raise ConnectionError("No active database connection.")
        entry = {"query": query, "params": params or {}}
        self._query_log.append(entry)
        # In production: cursor.execute(query, params); return cursor.fetchall()
        return {"rows": [], "query": query}

    def get_query_log(self) -> list:
        """Return a copy of all executed queries (useful for testing)."""
        return list(self._query_log)

    # ── Test helper ───────────────────────────────────────────────────────────

    @classmethod
    def _reset_instance(cls) -> None:
        """
        FOR TESTING ONLY — resets the singleton so tests can start clean.
        Must never be called in production code.
        """
        with cls._lock:
            cls._instance = None

    def __repr__(self) -> str:
        return (f"DatabaseConnection(host={self._host}, "
                f"db={self._database}, connected={self._connected})")


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    db1 = DatabaseConnection.get_instance()
    db2 = DatabaseConnection.get_instance()

    assert db1 is db2, "Singleton violated — two instances created!"
    print(f"Same instance: {db1 is db2}")
    print(db1)

    db1.execute("SELECT * FROM users WHERE role = %(role)s",
                {"role": "STUDENT"})
    print(f"Query log: {db2.get_query_log()}")  # same object → same log
