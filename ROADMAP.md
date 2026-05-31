# Project Roadmap — University Research Collaboration Platform

This document outlines the planned features and improvements for the platform, grouped by priority and development phase. Community contributions are welcome on any of these items — see [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

---

## Current Status — v1.0.0 (Complete)

- ✅ Domain model: User, ResearchProject, Document, Task, Message, Notification, Invitation
- ✅ Six creational design patterns (Simple Factory, Factory Method, Abstract Factory, Builder, Prototype, Singleton)
- ✅ Repository layer with in-memory HashMap storage and RepositoryFactory abstraction
- ✅ Service layer with full business logic enforcement
- ✅ REST API (FastAPI) — Users, Projects, Tasks — 19 endpoints
- ✅ Interactive Swagger UI at `/docs`
- ✅ 249 automated tests (unit + integration)
- ✅ CI/CD pipeline with GitHub Actions
- ✅ Branch protection on `main`

---

## Phase 2 — Persistence & Authentication (Next Sprint)

| Feature | Description | Difficulty | Label |
|---|---|---|---|
| PostgreSQL integration | Replace in-memory repositories with real database persistence using psycopg2 | Medium | `feature-request` |
| JWT Authentication | Add token-based authentication so API endpoints are secured | Medium | `feature-request` |
| User login endpoint | `POST /api/auth/login` returning a JWT token | Easy | `good-first-issue` |
| Password reset flow | Allow users to request a password reset via email | Medium | `feature-request` |
| Database migrations | Set up Alembic for schema versioning and migrations | Medium | `feature-request` |

---

## Phase 3 — Extended API Coverage

| Feature | Description | Difficulty | Label |
|---|---|---|---|
| Document upload endpoint | `POST /api/documents` with file validation (PDF/DOCX only, ≤50MB) | Medium | `feature-request` |
| Document version history | `GET /api/documents/{id}/versions` listing all versions | Easy | `good-first-issue` |
| Message endpoints | `POST /api/messages` and `GET /api/messages` for platform messaging | Medium | `feature-request` |
| Invitation endpoints | `POST /api/invitations` and `POST /api/invitations/{id}/accept` | Easy | `good-first-issue` |
| Notification endpoints | `GET /api/notifications` and `POST /api/notifications/{id}/read` | Easy | `good-first-issue` |
| Search and filtering | Add full-text search to project and user list endpoints | Medium | `feature-request` |

---

## Phase 4 — Performance & Scalability

| Feature | Description | Difficulty | Label |
|---|---|---|---|
| Redis caching | Cache frequently read data (e.g. user profiles, project lists) with Redis | Hard | `feature-request` |
| Async endpoints | Convert FastAPI routes to `async def` for improved throughput | Medium | `good-first-issue` |
| Pagination | Add `?page=` and `?limit=` query parameters to all list endpoints | Easy | `good-first-issue` |
| Rate limiting | Prevent API abuse by limiting requests per IP per minute | Medium | `feature-request` |
| Background task queue | Use Celery to handle email notifications and file processing asynchronously | Hard | `feature-request` |

---

## Phase 5 — Developer Experience

| Feature | Description | Difficulty | Label |
|---|---|---|---|
| Docker support | Add `Dockerfile` and `docker-compose.yml` for one-command local setup | Medium | `good-first-issue` |
| Postman collection | Export all API endpoints as a Postman collection for manual testing | Easy | `good-first-issue` |
| Linting with flake8 | Add flake8 to the CI pipeline to enforce code style automatically | Easy | `good-first-issue` |
| Pre-commit hooks | Set up pre-commit to run linting and tests before every commit | Easy | `good-first-issue` |
| API versioning | Prefix all routes with `/api/v1/` to support future breaking changes | Easy | `good-first-issue` |

---

## How to Contribute to the Roadmap

If you have an idea that is not listed here:

1. Open a GitHub Issue with the label `feature-request`.
2. Describe what the feature does and why it is valuable.
3. A maintainer will review it and add it to the roadmap if accepted.

All contributions — however small — are appreciated.
