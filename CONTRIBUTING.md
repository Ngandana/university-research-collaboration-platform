# Contributing to the University Research Collaboration Platform

Thank you for your interest in contributing! This document explains everything you need to get started, from setting up the project locally to submitting your first Pull Request.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Running Tests](#running-tests)
- [How to Pick an Issue](#how-to-pick-an-issue)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Code of Conduct](#code-of-conduct)

---

## Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.12+** — [Download here](https://www.python.org/downloads/)
- **Git** — [Download here](https://git-scm.com/)
- **VS Code** (recommended) — [Download here](https://code.visualstudio.com/)

---

## Local Setup

Follow these steps exactly to get the project running on your machine.

**1. Fork the repository**

Click the **Fork** button at the top right of this page. This creates your own copy of the project under your GitHub account.

**2. Clone your fork**

```bash
git clone https://github.com/YOUR-USERNAME/university-research-collaboration-platform.git
cd university-research-collaboration-platform
```

**3. Create a virtual environment**

```bash
# Windows
python -m venv .venv
.venv\Scripts\Activate.ps1

# Mac / Linux
python -m venv .venv
source .venv/bin/activate
```

**4. Install dependencies**

```bash
python -m pip install --upgrade pip
pip install fastapi uvicorn httpx pytest pytest-cov
```

**5. Run the tests to confirm everything works**

```bash
python -m pytest tests/ -v
```

You should see **249 passed**. If any tests fail, do not proceed — open an issue describing what went wrong.

**6. Run the API locally**

```bash
uvicorn api.main:app --reload
```

Then open `http://localhost:8000/docs` in your browser to see the interactive API documentation.

---

## Project Structure

```
university-research-collaboration-platform/
│
├── src/                          # Core domain classes (User, Project, Task, etc.)
├── services/                     # Business logic layer
├── api/                          # FastAPI REST API routes
├── repositories/                 # Repository interfaces and in-memory implementations
├── creational_patterns/          # Six creational design pattern implementations
├── factories/                    # Repository factory for storage abstraction
├── tests/
│   ├── api/                      # API integration tests
│   └── services/                 # Service layer unit tests
├── docs/                         # API documentation and OpenAPI schema
├── .github/workflows/ci.yml      # GitHub Actions CI/CD pipeline
├── CONTRIBUTING.md               # This file
├── ROADMAP.md                    # Planned features
├── CHANGELOG.md                  # Version history
└── README.md                     # Project overview
```

---

## Coding Standards

Please follow these standards so your code is consistent with the rest of the project.

### Style
- Follow **PEP 8** — Python's official style guide.
- Use **4 spaces** for indentation (no tabs).
- Maximum line length: **100 characters**.
- Use **descriptive variable names** — `user_repository` not `ur`.

### Docstrings
Every class and public method must have a docstring explaining what it does:

```python
def register_user(self, user_id: str, name: str, email: str) -> User:
    """
    Register a new user on the platform.
    Raises DuplicateEmailError if the email is already in use.
    """
```

### Type hints
All function parameters and return types must be annotated:

```python
def get_user(self, user_id: str) -> User:
```

### Tests
- Every new feature or bug fix **must include tests**.
- Tests go in `tests/services/` for service logic or `tests/api/` for API endpoints.
- Test function names must describe what they test: `test_register_user_duplicate_email_raises`.
- All 249 existing tests must still pass after your changes.

---

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run only service tests
python -m pytest tests/services/ -v

# Run only API tests
python -m pytest tests/api/ -v

# Run with coverage report
python -m pytest tests/ --cov=src --cov=services --cov=api --cov-report=term-missing
```

---

## How to Pick an Issue

1. Go to the [Issues tab](../../issues).
2. Filter by the label **`good-first-issue`** — these are simple, well-defined tasks ideal for first-time contributors.
3. Filter by **`feature-request`** for larger enhancements if you want a bigger challenge.
4. Comment on the issue saying "I'd like to work on this" so we know it's taken.
5. Wait for a maintainer to assign it to you before starting work.

---

## Submitting a Pull Request

**1. Create a branch from your fork**

```bash
git checkout -b feature/your-feature-name
```

Use a descriptive branch name:
- `feature/add-document-search` for new features
- `fix/task-overdue-status-bug` for bug fixes
- `docs/update-api-documentation` for documentation changes

**2. Make your changes**

Write your code, following the coding standards above. Add tests for everything you change.

**3. Run the full test suite**

```bash
python -m pytest tests/ -v
```

All 249 tests must pass plus your new ones.

**4. Commit with a clear message**

```bash
git add .
git commit -m "Add document search endpoint with title and status filters"
```

**5. Push and open a PR**

```bash
git push origin feature/your-feature-name
```

Then go to GitHub and click **Compare & pull request**. In your PR description include:
- What the change does.
- Which issue it closes (e.g. `Closes #21`).
- How you tested it.

**6. Respond to review feedback**

A maintainer will review your PR. Address any comments and push additional commits to the same branch — the PR updates automatically.

---

## Code of Conduct

- Be respectful and constructive in all comments and reviews.
- Focus feedback on the code, not the person.
- Beginners are welcome — no question is too simple.
- Discrimination or harassment of any kind will result in immediate removal from the project.
