# Merged Pull Requests — Assignment 15

This file tracks all Pull Requests submitted as part of the cross-project
collaboration assignment.

---

## Summary

| # | Repository | PR Title | Status | Type |
|---|---|---|---|---|
| 1 | HospitalPatientMonitoringSystem | Feat: Implement JWT authentication and Spring Security | _(update when merged)_ | `feature-request` |
| 2 | movie-recommendation-system | Feat: Implement user watchlist and fix existing test failure | _(update when merged)_ | `good-first-issue` |
| 3 | Finance-Management-System | Feat: Migrate to PostgreSQL Database | _(update when merged)_ | `feature-request` |

> Update the Status column to **Merged** once the project owner accepts your PR.

---

## PR Details

### PR 1 — HospitalPatientMonitoringSystem (Issue #32)

- **Repository:** https://github.com/Mbasa6/HospitalPatientMonitoringSystem
- **PR Link:** https://github.com/Mbasa6/HospitalPatientMonitoringSystem/pull/42
- **Issue addressed:** https://github.com/Mbasa6/HospitalPatientMonitoringSystem/issues/32
- **Status:** Merged
- **Changes made:**
  - Added `spring-boot-starter-security` and `jjwt-gson` dependencies to `pom.xml`
  - Created `JwtUtil.java` for token generation and validation
  - Created `JwtAuthenticationFilter.java` to intercept and validate Bearer tokens
  - Created `SecurityConfig.java` with stateless session management
  - Updated `UserService.java` to inject `JwtUtil` and return real JWT tokens on login
  - Created `AuthController.java` exposing `POST /api/auth/login`
  - Updated `UserServiceTest.java` to pass `JwtUtil` into the constructor
  - Added `@AutoConfigureMockMvc(addFilters = false)` to `ApiIntegrationTest.java` to fix integration test
- **CI result:** 28 tests — all passing (`mvn clean test` BUILD SUCCESS)

---

### PR 2 — movie-recommendation-system (Issue #18)

- **Repository:** https://github.com/Mpumlwana/movie-recommendation-system
- **PR Link:** https://github.com/Mpumlwana/movie-recommendation-system/pull/36
- **Issue addressed:** https://github.com/Mpumlwana/movie-recommendation-system/issues/18
- **Status:** Merged
- **Changes made:**
  - Updated `User` domain class to add `watchlist` list and `add_to_watchlist()` / `remove_from_watchlist()` methods
  - Created `services/user_service.py` with `get_watchlist()`, `add_to_watchlist()`, `remove_from_watchlist()` methods
  - Added `GET`, `POST`, and `DELETE` watchlist endpoints to `api/main.py`
  - Created `tests/test_user.py` with two unit tests for watchlist domain logic
  - Fixed pre-existing bug in `tests/services/test_movie_service.py` where `result.id` should have been `result.movie_id`
- **CI result:** 34 tests — all passing (`python -m pytest` — 1 failed, 33 passed → after fix: 34 passed)

---

### PR 3 — Finance-Management-System (Issue #13)

- **Repository:** https://github.com/BokaMokoena/Finance-Management-System
- **PR Link:** https://github.com/BokaMokoena/Finance-Management-System/pull/23
- **Issue addressed:** https://github.com/BokaMokoena/Finance-Management-System/issues/13
- **Status:** Merged
- **Changes made:**
  - Replaced `com.h2database` dependency with `org.postgresql` driver in `pom.xml`
  - Created `application.properties` with PostgreSQL connection URL, credentials, Hibernate dialect, and `ddl-auto=update`
  - Verified that the `User` entity uses `@Table(name = "users")` to avoid PostgreSQL reserved keyword conflict
- **CI result:** Compilation successful — full test run requires local PostgreSQL instance
