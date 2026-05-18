# API Documentation — University Research Collaboration Platform

**Version:** 1.0.0  
**Base URL:** `http://localhost:8000`  
**Interactive Swagger UI:** `http://localhost:8000/docs`  
**OpenAPI JSON:** `http://localhost:8000/openapi.json`

---

## How to run the API locally

```bash
pip install fastapi uvicorn httpx
uvicorn api.main:app --reload
```

Then open `http://localhost:8000/docs` in your browser to see the full interactive Swagger UI.

---

## Authentication

> This version uses in-memory storage with no authentication layer. Authentication (JWT tokens) is planned for a future sprint.

---

## Entities Covered

This API covers the three minimum required entities: **Users**, **Research Projects**, and **Tasks**.

---

## Error Response Format

All error responses follow this structure:

```json
{ "detail": "Human-readable error message." }
```

| HTTP Code | Meaning |
|---|---|
| `200` | OK |
| `201` | Created |
| `204` | No Content (successful delete) |
| `403` | Forbidden — user does not have permission |
| `404` | Not Found — entity does not exist |
| `409` | Conflict — e.g. duplicate email |
| `422` | Unprocessable Entity — validation or business rule failure |

---

## Users API  `/api/users`

### POST `/api/users` — Register a user

**Request body:**
```json
{
  "user_id": "u-001",
  "name": "Alice Dube",
  "email": "alice@uni.ac.za",
  "password": "securepass",
  "role": "student"
}
```
Valid roles: `student`, `supervisor`, `researcher`, `admin`.  
Password minimum: 6 characters. Email must be unique.

**Response `201`:**
```json
{
  "user_id": "u-001",
  "name": "Alice Dube",
  "email": "alice@uni.ac.za",
  "role": "STUDENT",
  "status": "ACTIVE",
  "created_date": "2026-05-18"
}
```

---

### GET `/api/users` — Get all users

Optional query parameter: `?role=supervisor`

**Response `200`:** Array of user objects.

---

### GET `/api/users/{user_id}` — Get user by ID

**Response `200`:** Single user object.  
**Response `404`:** User not found.

---

### PUT `/api/users/{user_id}` — Update profile

**Request body** (all fields optional):
```json
{ "name": "Alice Updated", "email": "new@uni.ac.za" }
```

**Response `200`:** Updated user.  
**Response `409`:** New email already in use.

---

### POST `/api/users/{user_id}/suspend` — Suspend user (admin)

**Response `200`:** User with status `SUSPENDED`.

---

### POST `/api/users/{user_id}/reactivate` — Reactivate user (admin)

**Response `200`:** User with status `ACTIVE`.

---

### DELETE `/api/users/{user_id}` — Deactivate user

**Response `204`:** No content.

---

## Projects API  `/api/projects`

### POST `/api/projects` — Create a project

**Request body:**
```json
{
  "project_id": "proj-001",
  "title": "AI in Education Research",
  "description": "Exploring AI applications.",
  "owner_id": "u-002"
}
```
Owner must be an ACTIVE `supervisor` or `researcher`.

**Response `201`:** Created project.  
**Response `403`:** Owner has wrong role.  
**Response `404`:** Owner not found.

---

### GET `/api/projects` — Get all projects

Optional filters: `?owner_id=u-002` or `?member_id=u-001`

---

### GET `/api/projects/{project_id}` — Get project by ID

**Response `404`:** Project not found.

---

### POST `/api/projects/{project_id}/members` — Add a member

**Request body:**
```json
{ "user_id": "u-001", "requestor_id": "u-002" }
```
`requestor_id` must be the project owner.

**Response `200`:** Updated project with new member count.

---

### POST `/api/projects/{project_id}/complete` — Complete a project

**Request body:**
```json
{ "requestor_id": "u-002" }
```

**Response `200`:** Project with status `COMPLETED`.  
**Response `403`:** Not the project owner.

---

### DELETE `/api/projects/{project_id}` — Delete a project

Query parameter: `?requestor_id=u-002`  
Project must not be ACTIVE.

**Response `204`:** No content.

---

## Tasks API  `/api/tasks`

### POST `/api/tasks` — Create a task

**Request body:**
```json
{
  "task_id": "task-001",
  "title": "Literature Review",
  "description": "Review 20 academic papers.",
  "deadline": "2026-06-30",
  "project_id": "proj-001",
  "creator_id": "u-002"
}
```
Creator must be `supervisor` or `researcher`. Deadline must be in the future.

**Response `201`:** Created task.

---

### GET `/api/tasks` — Get all tasks

Optional filters: `?project_id=proj-001`, `?assignee_id=u-001`, `?overdue=true`

---

### GET `/api/tasks/{task_id}` — Get task by ID

---

### POST `/api/tasks/{task_id}/assign` — Assign a task

**Request body:**
```json
{ "assignee_id": "u-001", "requestor_id": "u-002" }
```
Business rule: A student cannot have more than **10 active tasks** simultaneously.

**Response `200`:** Task with status `ASSIGNED`.

---

### POST `/api/tasks/{task_id}/start` — Start a task

**Request body:**
```json
{ "user_id": "u-001" }
```
Only the assigned user can start the task.

**Response `200`:** Task with status `IN_PROGRESS`.

---

### POST `/api/tasks/{task_id}/complete` — Complete a task

**Request body:**
```json
{ "user_id": "u-001" }
```

**Response `200`:** Task with status `COMPLETED`.

---

### DELETE `/api/tasks/{task_id}` — Delete a task

Query parameter: `?requestor_id=u-002`  
Cannot delete a task that is IN_PROGRESS or COMPLETED.

**Response `204`:** No content.

---

## Business Rules Enforced by the API

| Rule | Endpoint | HTTP response if violated |
|---|---|---|
| Email must be unique | `POST /api/users` | `409` |
| Password ≥ 6 characters | `POST /api/users` | `422` |
| Only supervisor/researcher can create projects | `POST /api/projects` | `403` |
| Only project owner can add members | `POST /api/projects/{id}/members` | `403` |
| Only supervisor/researcher can create/assign tasks | `POST /api/tasks`, `POST /api/tasks/{id}/assign` | `403` |
| Task deadline must be in the future | `POST /api/tasks` | `422` |
| Student max 10 active tasks | `POST /api/tasks/{id}/assign` | `422` |
| Only assigned user can start/complete task | `POST /api/tasks/{id}/start|complete` | `403` |
| Cannot delete ACTIVE project | `DELETE /api/projects/{id}` | `422` |
| Cannot delete IN_PROGRESS/COMPLETED task | `DELETE /api/tasks/{id}` | `422` |
