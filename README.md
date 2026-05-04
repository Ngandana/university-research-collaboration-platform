# University Research Collaboration Platform

## Project Overview

The University Research Collaboration Platform is a web-based system designed to support collaboration between students, supervisors, and researchers within a university environment. The platform allows users to create research projects, collaborate on documents, manage research tasks, and communicate within research teams.

Research collaboration within universities is often fragmented across emails, messaging platforms, and multiple document storage systems. This platform centralizes research activities into a single integrated system that enables efficient project coordination, document sharing, and communication.

The system aims to improve research productivity, enhance supervision processes, and support effective collaboration between academic stakeholders.

## Key Features

* Research project creation and management
* Supervisor and student collaboration
* Document sharing and version control
* Task assignment and progress tracking
* Notifications and messaging
* Secure user authentication and role management

## Kanban Board Implementation

A GitHub Project board was created using the Automated Kanban template to manage Agile workflows.

The board was customized by adding additional columns:

* Testing: To validate completed tasks
* Blocked: To identify tasks that cannot proceed

User stories from Assignment 6 were linked to the board as GitHub Issues, with labels and assignments applied to ensure traceability and organization.

This implementation demonstrates practical use of Agile project management using GitHub tools.


## Project Documentation

The full system documentation can be found in the following files:

* **System Specification:**
  [SPECIFICATION.md](SPECIFICATION.md)

* **System Architecture:**
  [ARCHITECTURE.md](ARCHITECTURE.md)

## Repository Purpose

This repository contains the system specification and architectural design for the University Research Collaboration Platform as part of a Software Engineering assignment focused on system modeling and architecture design.

## Additional Documentation

- Stakeholder Analysis:  
  [STAKEHOLDER_ANALYSIS.md](STAKEHOLDER_ANALYSIS.md)

- System Requirements:  
  [SYSTEM_REQUIREMENTS.md](SYSTEM_REQUIREMENTS.md)

- Reflection:  
  [REFLECTION.md](REFLECTION.md)


## Assignment 8: System Modeling

* [STATE_DIAGRAMS.md](STATE_DIAGRAMS.md)
* [ACTIVITY_DIAGRAMS.md](ACTIVITY_DIAGRAMS.md)
* [TRACEABILITY_A8.md](TRACEABILITY_A8.md)
* [REFLECTION_A8.md](REFLECTION_A8.md)

This section includes object state modeling and activity workflow modeling aligned with system requirements, use cases, and Agile planning.

## Assignment 9: Domain Modeling and Class Design

* [DOMAIN_MODEL.md](DOMAIN_MODEL.md)
* [CLASS_DIAGRAM.md](CLASS_DIAGRAM.md)
* [REFLECTION_A9.md](REFLECTION_A9.md)

This section includes domain modeling and class diagram development aligned with system requirements, workflows, and Agile planning.

## Assignment 10: Class Implementation & Creational Design Patterns

### Language Choice

**Python 3.12** was chosen for the following reasons:

- All prior assignments used Python-compatible pseudocode and Mermaid diagrams; Python keeps implementation closest to the designs already documented.
- Python's `abc` module provides clean abstract class / interface support for Factory Method and Abstract Factory patterns.
- Python's `copy.deepcopy` provides reliable deep cloning for the Prototype pattern.
- Python's `threading.Lock` enables thread-safe Singleton implementation verifiable with a 20-thread stress test.
- `pytest` + `pytest-cov` delivers professional-grade unit testing and coverage reporting with minimal boilerplate.

---

### Repository Structure

```
university-research-collaboration-platform/
│
├── src/                          # Core domain class implementations
│   ├── __init__.py
│   ├── user.py                   # User, UserRole, UserStatus
│   ├── research_project.py       # ResearchProject, ProjectStatus
│   ├── document.py               # Document, DocumentVersion, DocumentStatus
│   ├── task.py                   # Task, TaskStatus
│   └── communication.py          # Message, Notification, Invitation + enums
│
├── creational_patterns/          # All six creational pattern implementations
│   ├── __init__.py
│   ├── simple_factory.py         # UserFactory
│   ├── factory_method.py         # NotificationCreator + concrete creators
│   ├── abstract_factory.py       # StorageFactory + Local/Cloud variants
│   ├── builder.py                # ResearchProjectBuilder + Director
│   ├── prototype.py              # TaskPrototype + TaskCache
│   └── singleton.py              # DatabaseConnection (thread-safe)
│
├── tests/                        # Unit tests
│   ├── __init__.py
│   ├── test_creational_patterns.py   # 54 tests for all six patterns
│   └── test_src_classes.py           # 36 tests for core domain classes
│
├── CHANGELOG.md                  # Full change history
└── README.md                     # This file
```

---

### Running Tests

```bash
# Install dependencies
pip install pytest pytest-cov

# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src --cov=creational_patterns --cov-report=term-missing
```

**Results: 90 tests — all passing. Coverage: 83%.**

---

### Creational Pattern Rationale

| Pattern | Applied To | Justification |
|---|---|---|
| **Simple Factory** | `UserFactory` | All User objects share one class; only the `UserRole` enum differs. A single dispatch method is the correct weight — no need to subclass. Maps to FR2 (RBAC). |
| **Factory Method** | `NotificationCreator` + subclasses | Three notification types (Task, Message, Project) need different `NotificationType` values and message formats. Factory method lets each creator subclass decide construction. Maps to FR9 (Notifications). |
| **Abstract Factory** | `StorageFactory` → Local / Cloud | Document storage must switch between local (dev) and cloud (production) without changing call-site code. The factory produces a matched `FileStore` + `MetadataStore` pair. Maps to the Storage Container (Architecture doc) and FR5. |
| **Builder** | `ResearchProjectBuilder` + `ProjectDirector` | Projects have many optional configurations (end date, pre-loaded members, activation state). Builder eliminates telescoping constructors and provides fluent, readable construction. Maps to FR3. |
| **Prototype** | `TaskCache` + `TaskPrototype` | Research projects reuse standard task templates (Literature Review, Proposal, etc.). Cloning pre-configured prototypes is faster and safer than reconstructing from scratch. Maps to FR7. |
| **Singleton** | `DatabaseConnection` | The platform must share exactly one PostgreSQL connection pool. Multiple pools exhaust database connections. Thread-safe double-checked locking ensures correctness under concurrent load. Maps to NFR — Scalability. |

---

### GitHub Issue Updates (Assignment 10)

The following issues should be created and linked to commits for full marks:

| Issue | Title | Label |
|---|---|---|
| #11 | Implement core src/ classes from class diagram | `implementation`, `high` |
| #12 | Implement Simple Factory (UserFactory) | `pattern`, `high` |
| #13 | Implement Factory Method (NotificationCreator) | `pattern`, `high` |
| #14 | Implement Abstract Factory (StorageFactory) | `pattern`, `high` |
| #15 | Implement Builder (ResearchProjectBuilder) | `pattern`, `high` |
| #16 | Implement Prototype (TaskCache) | `pattern`, `medium` |
| #17 | Fix #17: Thread-safe Singleton (DatabaseConnection) | `pattern`, `high` |
| #18 | Write unit tests — all six patterns | `testing`, `high` |
| #19 | Write unit tests — core domain classes | `testing`, `medium` |
| #20 | Add CHANGELOG.md and update README | `documentation` |

**Commit message format:**
```
git commit -m "Fix #17: Thread-safe Singleton implementation with double-checked locking"
git commit -m "Close #18: Add 54 unit tests for all creational patterns"
```
