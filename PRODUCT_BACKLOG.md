# Product Backlog

## Introduction

This backlog prioritizes user stories using the MoSCoW method and includes effort estimates based on story points.

---

## Backlog Table

| Story ID | User Story      | Priority (MoSCoW) | Effort (Story Points) | Dependencies       |
| -------- | --------------- | ----------------- | --------------------- | ------------------ |
| US-001   | Login           | Must-have         | 3                     | None               |
| US-002   | Create Project  | Must-have         | 5                     | Login              |
| US-003   | Join Project    | Must-have         | 3                     | Login              |
| US-004   | Upload Document | Must-have         | 5                     | Join Project       |
| US-005   | Assign Tasks    | Must-have         | 5                     | Create Project     |
| US-008   | Manage Users    | Must-have         | 3                     | Login              |
| US-006   | Track Tasks     | Should-have       | 3                     | Assign Tasks       |
| US-007   | Messaging       | Should-have       | 3                     | Login              |
| US-009   | View Reports    | Could-have        | 5                     | All data available |
| US-010   | Data Encryption | Must-have         | 5                     | System-wide        |

---

## Prioritization Justification

Must-have stories are critical for delivering the Minimum Viable Product (MVP), including authentication, project creation, and core collaboration features.

Should-have stories enhance usability and collaboration but are not essential for initial deployment.

Could-have stories provide additional value such as analytics but can be deferred.

Security (data encryption) is prioritized as a must-have due to stakeholder concerns regarding data protection.
