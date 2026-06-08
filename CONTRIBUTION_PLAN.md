# Contribution Plan — Assignment 15

## Overview

This document outlines my strategy for contributing to peers' repositories as part of
Assignment 15: Cross-Project Contributions & Collaborative Development.

---

## Selected Projects

| # | Repository | Owner | Language | Issue Tackled |
|---|---|---|---|---|
| 1 | https://github.com/Mbasa6/HospitalPatientMonitoringSystem | Mbasa6 | Java / Spring Boot | #32 — JWT Authentication |
| 2 | https://github.com/Mpumlwana/movie-recommendation-system | Mpumlwana | Python / FastAPI | #18 — Add Watchlist Feature |
| 3 | https://github.com/BokaMokoena/Finance-Management-System | BokaMokoena | Java / Spring Boot | #13 — PostgreSQL Database |

---

## Selected Issues

| Project | Issue # | Title | Type | Status |
|---|---|---|---|---|
| HospitalPatientMonitoringSystem | #32 | Implement JWT Authentication | `feature-request` | PR Submitted |
| movie-recommendation-system | #18 | Add Watchlist Feature | `good-first-issue` | PR Submitted |
| Finance-Management-System | #13 | US-012: PostgreSQL Database | `feature-request` | PR Submitted |

---

## Contribution Strategy

### Phase 1 — Feature-Request (JWT Authentication)
Implemented Spring Security with JWT token generation and validation for the Hospital
Patient Monitoring System. This was an intermediate-level issue requiring new security
classes, updated service constructors, and fixing an existing integration test.

### Phase 2 — Feature Addition (Watchlist)
Added a complete watchlist feature to the movie recommendation system — domain model
update, new UserService, three REST endpoints, and two unit tests. Also fixed a
pre-existing failing test in the movie service as a bonus contribution.

### Phase 3 — Configuration Migration (PostgreSQL)
Migrated the Finance Management System from an in-memory H2 database to PostgreSQL
by updating the Maven dependency and creating the application.properties configuration.

### Communication approach
- Commented on each issue before starting work to claim it.
- Kept each PR focused on one feature only.
- Responded to build errors promptly and fixed them before pushing.
