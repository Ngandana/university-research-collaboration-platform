# Issue Labels — University Research Collaboration Platform

This document tracks all issues that have been labeled as `good-first-issue` or `feature-request` to help new contributors find suitable tasks quickly.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to get started.

---

## `good-first-issue` — Beginner Friendly Tasks

These issues are small, well-defined, and ideal for first-time contributors.

| Issue | Title | Phase |
|-------|-------|-------|
| #2 | US-002: Create Research Project | Sprint 1 – MVP |
| #3 | US-003: Join Research Project | Sprint 1 – MVP |
| #4 | US-004: Upload Research Document | Sprint 1 – MVP |
| #5 | US-005: Assign Tasks to Students | Sprint 1 – MVP |
| Phase 2 | User login endpoint — `POST /api/auth/login` returning a JWT token | Persistence & Auth |
| Phase 3 | Document version history — `GET /api/documents/{id}/versions` | Extended API |
| Phase 3 | Invitation endpoints — `POST /api/invitations` and accept | Extended API |
| Phase 3 | Notification endpoints — `GET /api/notifications` and mark as read | Extended API |
| Phase 4 | Async endpoints — Convert FastAPI routes to `async def` | Performance |
| Phase 4 | Pagination — Add `?page=` and `?limit=` to list endpoints | Performance |
| Phase 5 | Docker support — Add `Dockerfile` and `docker-compose.yml` | Dev Experience |
| Phase 5 | Postman collection — Export all endpoints for manual testing | Dev Experience |
| Phase 5 | Linting with flake8 — Add flake8 to CI pipeline | Dev Experience |
| Phase 5 | Pre-commit hooks — Run linting and tests before every commit | Dev Experience |
| Phase 5 | API versioning — Prefix all routes with `/api/v1/` | Dev Experience |

---

## `feature-request` — New Features & Enhancements

These issues involve building new functionality and are suited for contributors with more experience.

| Issue | Title | Phase |
|-------|-------|-------|
| #6 | US-006: Track Task Progress | Sprint 1 – MVP |
| #7 | US-007: Send Messages | Sprint 1 – MVP |
| #9 | US-009: View Reports | Sprint 1 – MVP |
| Phase 2 | PostgreSQL integration — Replace in-memory storage with real DB | Persistence & Auth |
| Phase 2 | JWT Authentication — Secure all API endpoints with tokens | Persistence & Auth |
| Phase 2 | Password reset flow — Allow users to reset via email | Persistence & Auth |
| Phase 2 | Database migrations — Set up Alembic for schema versioning | Persistence & Auth |
| Phase 3 | Document upload endpoint — `POST /api/documents` with validation | Extended API |
| Phase 3 | Message endpoints — `POST` and `GET /api/messages` | Extended API |
| Phase 3 | Search and filtering — Full-text search on projects and users | Extended API |
| Phase 4 | Redis caching — Cache user profiles and project lists | Performance |
| Phase 4 | Rate limiting — Limit requests per IP per minute | Performance |
| Phase 4 | Background task queue — Use Celery for async notifications | Performance |

---

## `security` — Security-Critical Issues

| Issue | Title | Priority |
|-------|-------|----------|
| #10 | US-010: Encrypt User Data | High |

---

## How Labels Help

- **`good-first-issue`** — Pick these if you are new to the project. They are small and self-contained.
- **`feature-request`** — Pick these if you want to build something new and impactful.
- **`security`** — These require careful review before merging. Discuss your approach in the issue first.

---

*Labels applied as part of Issue #61 — improving contributor discoverability.*