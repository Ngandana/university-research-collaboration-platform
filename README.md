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



# Assignment 11 – README Addition

> **Add this section to your existing README.md** beneath the Assignment 10 entry.

---

## Assignment 11: Persistence Repository Layer

### Design Rationale

**Why a generic `Repository[T, ID]` interface?**
A single generic base interface means all CRUD method signatures are defined once. Entity-specific interfaces (e.g. `UserRepository`) simply extend it and add domain queries (`find_by_email`, `find_overdue`, etc.). Without generics, every repository would re-declare identical `save`, `find_by_id`, `find_all`, `delete`, `exists`, and `count` signatures — pure duplication.

**Why Factory Pattern (not pure DI)?**
The `RepositoryFactory` was chosen over a Dependency Injection container because the system needs to support runtime switching between backends (tests use `MEMORY`; production would use `DATABASE`). A factory centralises that decision in one file. Adding a new backend (e.g. `REDIS`) requires only one new case in the factory and one new implementation file — all existing service code is unchanged.

**Why in-memory HashMap first?**
In-memory repositories are fast, have no external dependencies, and make unit tests reliable and repeatable. They prove the interface contract works before any database is involved. The `RepositoryFactory` means switching to a real database later requires changing one line at the call site: `"MEMORY"` → `"DATABASE"`.

---

### Repository Structure (Assignment 11 additions)

```
university-research-collaboration-platform/
│
├── repositories/
│   ├── interfaces.py              # Generic + entity-specific interfaces
│   ├── stubs.py                   # FileSystem + Database stubs (future)
│   └── inmemory/
│       └── implementations.py     # HashMap-based implementations (all 6 entities)
│
├── factories/
│   └── repository_factory.py      # Storage-abstraction factory
│
├── tests/
│   ├── test_repositories.py       # 66 tests for all repos + factory
│   ...
│
└── CHANGELOG.md
```

---

### Running Repository Tests

```bash
pytest tests/test_repositories.py -v
```

Expected output: **66 passed**.

---

### GitHub Issues (Assignment 11)

Create and close these issues, linking each commit:

| Issue | Title | Label |
|---|---|---|
| #21 | Design generic Repository interface | `architecture`, `high` |
| #22 | Implement entity-specific repository interfaces | `architecture`, `high` |
| #23 | Implement InMemoryUserRepository | `implementation`, `high` |
| #24 | Implement InMemoryResearchProjectRepository | `implementation`, `high` |
| #25 | Implement InMemoryDocumentRepository | `implementation`, `medium` |
| #26 | Implement InMemoryTaskRepository | `implementation`, `medium` |
| #27 | Implement InMemoryMessageRepository | `implementation`, `medium` |
| #28 | Implement InMemoryInvitationRepository | `implementation`, `medium` |
| #29 | Implement RepositoryFactory (storage abstraction) | `pattern`, `high` |
| #30 | Add FileSystem + Database stubs (future-proofing) | `future`, `low` |
| #31 | Write unit tests for repository layer (66 tests) | `testing`, `high` |
| #32 | Update CHANGELOG and README for Assignment 11 | `documentation` |

**Commit message format:**
```
git commit -m "Close #23: Implement InMemoryUserRepository with HashMap storage"
git commit -m "Close #29: Add RepositoryFactory for MEMORY/FILESYSTEM/DATABASE switching"
```

---

### Future Storage Backends

The stubs in `repositories/stubs.py` document exactly what needs to be implemented to activate each backend:

**FileSystem** — serialize entities to JSON using `json.dump` / `json.load`. Each entity type maps to one JSON file. Requires `to_dict()` / `from_dict()` methods on domain classes.

**Database** — persist to PostgreSQL using `psycopg2` or SQLAlchemy. Connects via the `DatabaseConnection` singleton already implemented in `creational_patterns/singleton.py`. Full table schemas are documented in each stub class.


# Assignment 12 – README Addition


---

## Assignment 12: Service Layer and REST API

### Framework Choice

**FastAPI (Python)** was chosen because:
- It auto-generates interactive Swagger UI from the code — no separate documentation tool needed (satisfies the API documentation requirement out of the box).
- Pydantic models provide request/response validation with clear error messages.
- The `TestClient` allows full integration tests without running a live server, keeping CI fast.
- It integrates cleanly with the existing Python codebase from Assignments 9–11.

### Architecture

```
HTTP Request
    ↓
FastAPI Route (api/main.py)      ← validates HTTP input (Pydantic)
    ↓
Service Layer (services/)        ← enforces business rules
    ↓
Repository Layer (repositories/) ← persists/retrieves data
    ↓
Domain Model (src/)              ← entity state and behaviour
```

### Repository Structure (Assignment 12 additions)

```
university-research-collaboration-platform/
│
├── services/
│   ├── user_service.py          # UserService + custom exceptions
│   ├── project_service.py       # ProjectService + custom exceptions
│   └── task_service.py          # TaskService + custom exceptions
│
├── api/
│   └── main.py                  # FastAPI app — all routes + Pydantic schemas
│
├── docs/
│   ├── openapi.json             # Auto-generated OpenAPI 3.1 schema
│   └── API_DOCUMENTATION.md    # Full endpoint reference
│
├── tests/
│   ├── services/
│   │   └── test_services.py     # 50 unit tests for service layer
│   └── api/
│       └── test_api.py          # 43 integration tests for REST API
│
└── CHANGELOG.md
```

### Running the API

```bash
pip install fastapi uvicorn httpx
uvicorn api.main:app --reload
```

Visit:
- **Swagger UI:** http://localhost:8000/docs
- **OpenAPI JSON:** http://localhost:8000/openapi.json
- **Health check:** http://localhost:8000/health

### Running All Tests

```bash
python -m pytest tests/ -v
```

Expected: **93 passed** (50 service + 43 API integration tests).

---

### GitHub Issues (Assignment 12)

| Issue | Title | Label |
|---|---|---|
| #33 | Implement UserService with business logic | `service`, `high` |
| #34 | Implement ProjectService with business logic | `service`, `high` |
| #35 | Implement TaskService with business logic | `service`, `high` |
| #36 | Build FastAPI app with User endpoints | `api`, `high` |
| #37 | Build FastAPI app with Project endpoints | `api`, `high` |
| #38 | Build FastAPI app with Task endpoints | `api`, `high` |
| #39 | Write unit tests for all service classes (50 tests) | `testing`, `high` |
| #40 | Write integration tests for all API endpoints (43 tests) | `testing`, `high` |
| #41 | Generate OpenAPI docs and API_DOCUMENTATION.md | `documentation` |
| #42 | Update CHANGELOG and README for Assignment 12 | `documentation` |

**Commit message format:**
```
git commit -m "Close #33: Implement UserService with register, suspend, reactivate"
git commit -m "Close #36: Add FastAPI User endpoints with Pydantic validation"
```

## Assignment 13: CI/CD with GitHub Actions

### Running Tests Locally

```bash
# Activate your virtual environment first
.venv\Scripts\Activate.ps1       # Windows PowerShell
source .venv/bin/activate        # Mac/Linux

# Install dependencies
python -m pip install fastapi uvicorn httpx pytest pytest-cov

# Run all tests
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ --cov=src --cov=services --cov=api --cov-report=term-missing
```

Expected result: **249 passed**

---

### How the CI/CD Pipeline Works

The pipeline is defined in `.github/workflows/ci.yml` and has two jobs:

#### Job 1 — `Run Tests` (CI)
**Triggers:** Every push to any branch, and every Pull Request targeting `main`.

Steps:
1. Checks out the repository.
2. Sets up Python 3.12.
3. Caches pip dependencies for speed.
4. Installs all dependencies.
5. Runs all 249 tests with coverage reporting.
6. Uploads `test-results.xml` and `coverage.xml` as artifacts.

If any test fails, this job fails — and because it is a required status check,
the PR merge button is blocked automatically.

#### Job 2 — `Build Release Artifact` (CD)
**Triggers:** Only when code is pushed/merged to `main` AND Job 1 passes.

Steps:
1. Builds a Python wheel (`.whl`) package of the entire platform.
2. Uploads the wheel as a downloadable artifact in GitHub Actions (retained 30 days).
3. If a Git tag is pushed (e.g. `v1.0.0`), also creates a GitHub Release.

---

### Branch Protection Rules

The `main` branch is protected with the following rules:

- Pull Request required before merging (minimum 1 reviewer approval).
- `Run Tests` CI job must pass before merge is allowed.
- Branches must be up to date with `main` before merging.
- Direct pushes to `main` are blocked for everyone including administrators.

See `PROTECTION.md` for full justification of each rule.

---

### CI/CD File Structure

```
university-research-collaboration-platform/
│
├── .github/
│   └── workflows/
│       └── ci.yml          # CI/CD pipeline definition
│
├── requirements.txt         # All Python dependencies
├── PROTECTION.md            # Branch protection justification
└── README.md                # This file
```

---

### GitHub Issues (Assignment 13)

| Issue | Title | Label |
|---|---|---|
| #43 | Create .github/workflows/ci.yml with test automation | `ci`, `high` |
| #44 | Add CD job to build Python wheel on main merge | `cd`, `high` |
| #45 | Configure branch protection rules on main | `devops`, `high` |
| #46 | Add requirements.txt for CI dependency installation | `devops` |
| #47 | Write PROTECTION.md justifying branch protection rules | `documentation` |
| #48 | Update README with CI/CD and local test instructions | `documentation` |

**Commit format:**
```
git commit -m "Close #43: Add GitHub Actions CI workflow with 249 test run"
git commit -m "Close #44: Add CD job to build and upload Python wheel artifact"
```

# Assignment 14 – README Addition

> **Add this section to your existing README.md** beneath the Assignment 13 entry.
> Also add the badges and Getting Started section near the TOP of your README, just below the project title.

---

## Badges (paste near the top of README, below the title)

![CI/CD](https://github.com/Ngandana/university-research-collaboration-platform/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Tests](https://img.shields.io/badge/tests-249%20passing-brightgreen)

---

## Getting Started

### Prerequisites
- Python 3.12+
- Git

### Installation

```bash
# 1. Fork this repo, then clone your fork
git clone https://github.com/YOUR-USERNAME/university-research-collaboration-platform.git
cd university-research-collaboration-platform

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows
source .venv/bin/activate          # Mac/Linux

# 3. Install dependencies
pip install fastapi uvicorn httpx pytest pytest-cov

# 4. Run the tests
python -m pytest tests/ -v

# 5. Start the API
uvicorn api.main:app --reload
```

Visit `http://localhost:8000/docs` for the interactive API documentation.

---

## Features Available for Contribution

| Feature | Difficulty | Issue Label |
|---|---|---|
| Add login endpoint (`POST /api/auth/login`) | Easy | `good-first-issue` |
| Add pagination to list endpoints | Easy | `good-first-issue` |
| Add Dockerfile for one-command setup | Easy | `good-first-issue` |
| Add document upload endpoint | Medium | `feature-request` |
| Add message and notification endpoints | Medium | `feature-request` |
| Integrate PostgreSQL database | Medium | `feature-request` |
| Add Redis caching layer | Hard | `feature-request` |

See [ROADMAP.md](ROADMAP.md) for the full list of planned features.

---

## Assignment 14: Open-Source Preparation

### Files Added

| File | Purpose |
|---|---|
| `CONTRIBUTING.md` | Setup instructions, coding standards, PR process |
| `ROADMAP.md` | Planned features grouped by development phase |
| `LICENSE` | MIT License |
| `VOTING_RESULTS.md` | Peer engagement tracking (stars, forks, feedback) |
| `REFLECTION.md` | 500+ word reflection on open-source collaboration |

### GitHub Issues Labelled for Contributors

Go to the [Issues tab](../../issues) and filter by:
- `good-first-issue` — simple, self-contained tasks for new contributors
- `feature-request` — larger enhancements listed in the roadmap

### Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a Pull Request.

### License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
