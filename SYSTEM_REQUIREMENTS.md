# System Requirements Document (SRD)

## Overview

This document defines the functional and non-functional requirements for the University Research Collaboration Platform.

---

# 1. Functional Requirements

### FR1: User Registration and Authentication

The system shall allow users to register and log in securely.

* Acceptance Criteria:

  * Users must provide email and password.
  * Authentication must validate credentials before access.

### FR2: Role-Based Access Control

The system shall assign roles (Student, Supervisor, Researcher, Admin).

* Acceptance Criteria:

  * Users can only access features permitted by their role.

### FR3: Create Research Project

The system shall allow supervisors and researchers to create projects.

* Acceptance Criteria:

  * Project must include title, description, and members.

### FR4: Join Research Project

The system shall allow users to join projects via invitation.

* Acceptance Criteria:

  * Only invited users can join a project.

### FR5: Document Upload

The system shall allow users to upload research documents.

* Acceptance Criteria:

  * Supported formats: PDF, DOCX.
  * File size limit enforced.

### FR6: Document Version Control

The system shall maintain version history of documents.

* Acceptance Criteria:

  * Users can view previous versions.

### FR7: Task Assignment

The system shall allow supervisors to assign tasks.

* Acceptance Criteria:

  * Tasks must include deadline and assignee.

### FR8: Task Tracking

The system shall track task progress.

* Acceptance Criteria:

  * Tasks must display status (Pending, In Progress, Completed).

### FR9: Messaging System

The system shall allow users to send messages within projects.

* Acceptance Criteria:

  * Messages must be delivered in real time.

### FR10: Notifications

The system shall notify users of updates.

* Acceptance Criteria:

  * Notifications triggered by task updates and messages.

---

# 2. Non-Functional Requirements

## Usability

* The system shall provide an intuitive user interface.
* The system shall be accessible on desktop and mobile devices.

## Deployability

* The system shall be deployable on cloud platforms.
* The system shall support Linux-based servers.

## Maintainability

* The system shall include well-documented APIs.
* The system shall follow modular architecture.

## Scalability

* The system shall support at least 1000 concurrent users.
* The system shall allow horizontal scaling.

## Security

* The system shall encrypt user data using secure protocols.
* The system shall implement authentication and authorization.

## Performance

* The system shall respond to user actions within 2 seconds.
* File uploads shall complete within acceptable time limits.
