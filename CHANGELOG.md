# CHANGELOG

All notable changes to the University Research Collaboration Platform are documented here.

---

## [Assignment 11] – Persistence Repository Layer

### Added – Repository Interfaces (`/repositories/interfaces.py`)

- `Repository[T, ID]` — generic abstract base with `save`, `find_by_id`, `find_all`, `delete`, `exists`, `count`.
- `UserRepository` — extends generic base; adds `find_by_email`, `find_by_role`, `find_by_status`.
- `ResearchProjectRepository` — adds `find_by_owner`, `find_by_status`, `find_by_member`.
- `DocumentRepository` — adds `find_by_project`, `find_by_status`, `find_by_uploader`.
- `TaskRepository` — adds `find_by_project`, `find_by_assignee`, `find_by_status`, `find_overdue`.
- `MessageRepository` — adds `find_by_sender`, `find_by_recipient`, `find_unread`.
- `InvitationRepository` — adds `find_by_project`, `find_by_recipient`, `find_pending`.

### Added – In-Memory Implementations (`/repositories/inmemory/implementations.py`)

- `InMemoryUserRepository` — HashMap dict; all CRUD + domain queries implemented.
- `InMemoryResearchProjectRepository` — HashMap dict; member and owner index queries.
- `InMemoryDocumentRepository` — HashMap dict + project/uploader index dicts.
- `InMemoryTaskRepository` — HashMap dict + project index dict.
- `InMemoryMessageRepository` — HashMap dict; unread filter via MessageStatus.
- `InMemoryInvitationRepository` — HashMap dict; pending filter via InvitationStatus.

### Added – Storage Abstraction (`/factories/repository_factory.py`)

- `RepositoryFactory` — static factory methods per entity type; dispatches to correct implementation based on `storage_type` string (`MEMORY`, `FILESYSTEM`, `DATABASE`).
- `_validate()` — central validation of storage type strings; case-insensitive; raises `ValueError` for unknown types.

### Added – Future-Proofing Stubs (`/repositories/stubs.py`)

- `FileSystemUserRepository` — stub with JSON load/flush skeleton; raises `NotImplementedError` with implementation instructions.
- `FileSystemResearchProjectRepository` — stub; notes on member serialization approach.
- `DatabaseUserRepository` — stub with full PostgreSQL schema comment (CREATE TABLE).
- `DatabaseResearchProjectRepository` — stub with junction table schema for project members.

### Added – Tests (`/tests/test_repositories.py`)

- 66 unit tests across all 6 repository implementations and the RepositoryFactory.
- Covers: save/find/delete/exists/count, all domain-specific queries, edge cases (missing IDs, empty repos, no-op deletes, read vs unread messages, overdue tasks, pending invitations).
- Factory tests verify correct type returned per backend, invalid type raises, stubs raise on use, independent instances per call.
- **All 66 tests passing.**

---

## [Assignment 10] – Class Implementation & Creational Patterns

- 5 core domain classes (`/src`).
- 6 creational pattern implementations (`/creational_patterns`).
- 90 unit tests — all passing, 83% coverage.
- `CHANGELOG.md`, `README_ADDITION.md`.

## [Assignment 9] – Domain Model & Class Diagram

- `DOMAIN_MODEL.md`, `CLASS_DIAGRAM.md`, `REFLECTION_A9.md`.

## [Assignments 3–8] — Architecture, Requirements, Use Cases, Agile, Diagrams

- See prior CHANGELOG entries in the repository.
