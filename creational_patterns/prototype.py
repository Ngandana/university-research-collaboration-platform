"""
prototype.py
Pattern: Prototype
──────────────────────────────────────────────────────────────────────────────
Use case: Cloning Task templates.

Research projects often reuse standard task sets (e.g. "Literature Review",
"Submit Draft", "Supervisor Feedback").  Rather than reconstructing them from
scratch each time, a TaskCache stores pre-configured prototype Tasks and
returns deep clones on request.  This avoids repeating costly initialisation
and ensures that clones do not share mutable state with the originals.

This maps to FR7 (Task Assignment) and the Sprint Plan (Assignment 6) where
repeatable sprint tasks are defined.
"""

import copy
from datetime import date, timedelta
from typing import Dict

from src.task import Task, TaskStatus
from src.user import User


# ── Prototype interface ───────────────────────────────────────────────────────

class Cloneable:
    """Mixin that adds a clone() method using deep copy."""

    def clone(self) -> "Cloneable":
        """Return a deep copy of this object."""
        return copy.deepcopy(self)


# ── Prototype-aware Task ──────────────────────────────────────────────────────

class TaskPrototype(Task, Cloneable):
    """
    A Task subclass that supports cloning.
    Inherits all Task behaviour; adds clone() via Cloneable mixin.
    """
    pass


# ── Task Cache (Prototype Registry) ──────────────────────────────────────────

class TaskCache:
    """
    Stores prototype Tasks and returns clones on demand.
    Clones are independent objects — changes to a clone do not affect the prototype.
    """

    def __init__(self):
        self._cache: Dict[str, TaskPrototype] = {}

    def register(self, key: str, prototype: TaskPrototype) -> None:
        """Register a prototype under a named key."""
        self._cache[key] = prototype

    def get_clone(self, key: str, new_task_id: str,
                  new_deadline: date = None) -> TaskPrototype:
        """
        Return a deep clone of the registered prototype.
        Optionally override task_id and deadline to make it unique.

        Raises:
            KeyError: If the key is not registered.
        """
        if key not in self._cache:
            raise KeyError(f"No task prototype registered for key '{key}'.")

        clone: TaskPrototype = self._cache[key].clone()
        clone._task_id = new_task_id  # assign fresh ID
        if new_deadline:
            clone._deadline = new_deadline
        clone._status = TaskStatus.CREATED  # reset state for fresh task
        clone._assigned_to = None
        return clone

    def list_prototypes(self) -> list:
        return list(self._cache.keys())


# ── Factory helper to build the default cache ─────────────────────────────────

def build_default_task_cache(dummy_supervisor: User) -> TaskCache:
    """
    Build a TaskCache pre-loaded with standard research-project task templates.
    Used at application startup.
    """
    cache = TaskCache()

    cache.register("literature_review", TaskPrototype(
        task_id="proto-lr",
        title="Literature Review",
        description="Identify and review at least 20 relevant academic papers.",
        deadline=date.today() + timedelta(days=14),
        created_by=dummy_supervisor,
    ))

    cache.register("research_proposal", TaskPrototype(
        task_id="proto-rp",
        title="Submit Research Proposal",
        description="Draft and submit a 2000-word research proposal.",
        deadline=date.today() + timedelta(days=21),
        created_by=dummy_supervisor,
    ))

    cache.register("progress_report", TaskPrototype(
        task_id="proto-pr",
        title="Submit Progress Report",
        description="Write a mid-project progress report for supervisor review.",
        deadline=date.today() + timedelta(days=60),
        created_by=dummy_supervisor,
    ))

    cache.register("final_submission", TaskPrototype(
        task_id="proto-fs",
        title="Final Submission",
        description="Submit the completed research paper and supporting materials.",
        deadline=date.today() + timedelta(days=120),
        created_by=dummy_supervisor,
    ))

    return cache


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from creational_patterns.simple_factory import UserFactory

    supervisor = UserFactory.create_user("u1", "Prof Nkosi",
                                         "nkosi@uni.ac.za", "pw", "supervisor")
    supervisor.register()

    cache = build_default_task_cache(supervisor)
    print("Registered prototypes:", cache.list_prototypes())

    task1 = cache.get_clone("literature_review", "t-001",
                            date.today() + timedelta(days=10))
    task2 = cache.get_clone("literature_review", "t-002",
                            date.today() + timedelta(days=20))

    print(task1)
    print(task2)

    # Prove independence — mutating clone does not affect prototype
    task1._title = "Modified Clone"
    original = cache.get_clone("literature_review", "t-003")
    assert original.title == "Literature Review", "Prototype was mutated — ERROR"
    print("Prototype integrity confirmed.")
