"""
builder.py
Pattern: Builder
──────────────────────────────────────────────────────────────────────────────
Use case: Step-by-step construction of a ResearchProject.

Creating a ResearchProject involves many optional attributes: description,
end date, initial members, initial tasks. The Builder pattern lets callers
compose a project incrementally without needing a constructor with many
optional parameters (telescoping constructor anti-pattern).

This maps to FR3 (Create Research Project) and UC6 (Create Project use case).
"""

from datetime import date
from typing import List, Optional, TYPE_CHECKING

from src.research_project import ResearchProject, ProjectStatus
from src.user import User
from src.task import Task, TaskStatus

if TYPE_CHECKING:
    pass


# ── Product ───────────────────────────────────────────────────────────────────

class ProjectBlueprint:
    """
    The complex object assembled by the builder.
    Wraps a ResearchProject with pre-configured initial tasks and members.
    """

    def __init__(self):
        self.project: Optional[ResearchProject] = None
        self.initial_tasks: List[Task] = []
        self.initial_members: List[User] = []

    def __repr__(self) -> str:
        return (f"ProjectBlueprint(project={self.project}, "
                f"tasks={len(self.initial_tasks)}, "
                f"members={len(self.initial_members)})")


# ── Abstract Builder ──────────────────────────────────────────────────────────

class ProjectBuilder:
    """Abstract builder interface."""

    def set_basic_info(self, project_id: str, title: str,
                       description: str, owner: User) -> "ProjectBuilder":
        raise NotImplementedError

    def set_end_date(self, end_date: date) -> "ProjectBuilder":
        raise NotImplementedError

    def add_member(self, user: User) -> "ProjectBuilder":
        raise NotImplementedError

    def add_task(self, task: Task) -> "ProjectBuilder":
        raise NotImplementedError

    def activate(self) -> "ProjectBuilder":
        raise NotImplementedError

    def build(self) -> ProjectBlueprint:
        raise NotImplementedError


# ── Concrete Builder ──────────────────────────────────────────────────────────

class ResearchProjectBuilder(ProjectBuilder):
    """
    Concrete builder for ResearchProject.
    Each method returns self for fluent (chained) calls.
    """

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._blueprint = ProjectBlueprint()
        self._project_id = None
        self._title = None
        self._description = ""
        self._owner = None
        self._end_date = None
        self._members: List[User] = []
        self._tasks: List[Task] = []
        self._activate = False

    def set_basic_info(self, project_id: str, title: str,
                       description: str, owner: User) -> "ResearchProjectBuilder":
        if not project_id or not title:
            raise ValueError("project_id and title are required.")
        self._project_id = project_id
        self._title = title
        self._description = description
        self._owner = owner
        return self

    def set_end_date(self, end_date: date) -> "ResearchProjectBuilder":
        if end_date < date.today():
            raise ValueError("End date cannot be in the past.")
        self._end_date = end_date
        return self

    def add_member(self, user: User) -> "ResearchProjectBuilder":
        self._members.append(user)
        return self

    def add_task(self, task: Task) -> "ResearchProjectBuilder":
        self._tasks.append(task)
        return self

    def activate(self) -> "ResearchProjectBuilder":
        self._activate = True
        return self

    def build(self) -> ProjectBlueprint:
        if not self._project_id or not self._owner:
            raise ValueError("set_basic_info() must be called before build().")

        project = ResearchProject(
            project_id=self._project_id,
            title=self._title,
            description=self._description,
            owner=self._owner,
        )

        if self._activate:
            project.activate()

        for member in self._members:
            project.add_member(member)

        self._blueprint.project = project
        self._blueprint.initial_tasks = list(self._tasks)
        self._blueprint.initial_members = project.get_members()

        result = self._blueprint
        self.reset()  # builder ready for reuse
        return result


# ── Director ──────────────────────────────────────────────────────────────────

class ProjectDirector:
    """
    Director — knows the construction sequences for common project types.
    Decouples the caller from knowing which builder steps to call.
    """

    def __init__(self, builder: ProjectBuilder):
        self._builder = builder

    def build_minimal_project(self, project_id: str, title: str,
                               owner: User) -> ProjectBlueprint:
        """A draft project with no end date, no extra members."""
        return (self._builder
                .set_basic_info(project_id, title, "", owner)
                .build())

    def build_active_project(self, project_id: str, title: str,
                              description: str, owner: User,
                              members: List[User],
                              end_date: date) -> ProjectBlueprint:
        """A fully configured, immediately active project."""
        builder = self._builder.set_basic_info(
            project_id, title, description, owner
        ).set_end_date(end_date).activate()
        for m in members:
            builder = builder.add_member(m)
        return builder.build()


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from creational_patterns.simple_factory import UserFactory
    from datetime import timedelta

    supervisor = UserFactory.create_user("u1", "Prof Nkosi",
                                         "nkosi@uni.ac.za", "pw", "supervisor")
    supervisor.register()
    student = UserFactory.create_user("u2", "Alice",
                                      "alice@uni.ac.za", "pw", "student")
    student.register()

    builder = ResearchProjectBuilder()
    director = ProjectDirector(builder)

    draft = director.build_minimal_project("p1", "AI in Education", supervisor)
    print("Draft:", draft)

    active = director.build_active_project(
        "p2", "Cloud Computing Research",
        "Exploring Huawei Cloud services",
        supervisor, [student],
        date.today() + timedelta(days=180),
    )
    print("Active:", active)
