# System Architecture

## Project Title

University Research Collaboration Platform

## Domain

Education / Academic Research Management

## Problem Statement

Universities require a centralized system that enables efficient collaboration between students, supervisors, and researchers during research projects. Without a structured platform, research teams rely on multiple disconnected tools for communication, document sharing, and task management. This fragmentation leads to inefficiencies and reduced research productivity.

The University Research Collaboration Platform provides a unified system where research teams can manage projects, share documents, assign tasks, and communicate effectively.

## Individual Scope

This project focuses on the architectural design of the system using the C4 model to illustrate how the system components interact and how the platform supports research collaboration workflows.

---

# C4 Architecture Model

The architecture of the system is modeled using the C4 model which includes the following levels:

1. System Context Diagram
2. Container Diagram
3. Component Diagram

---

# System Context Diagram

```mermaid
C4Context
title System Context Diagram for University Research Collaboration Platform

Person(student, "Student", "Conducts research and collaborates with supervisors")
Person(supervisor, "Supervisor", "Guides and monitors research projects")
Person(researcher, "Researcher", "Collaborates on academic research")
Person(admin, "Administrator", "Manages users and system operations")

System(platform, "Research Collaboration Platform", "Manages research projects, documents and collaboration")

Rel(student, platform, "Uses")
Rel(supervisor, platform, "Supervises research through")
Rel(researcher, platform, "Collaborates using")
Rel(admin, platform, "Administers")
```

---

# Container Diagram

```mermaid
C4Container
title Container Diagram for Research Collaboration Platform

Person(student, "Student")
Person(supervisor, "Supervisor")
Person(admin, "Administrator")

System_Boundary(system, "Research Collaboration Platform") {

Container(webapp, "Web Application", "React / Web UI", "User interface for students, supervisors and researchers")

Container(api, "Backend API", "Node.js / Python", "Handles business logic and system operations")

Container(auth, "Authentication Service", "JWT/Auth Service", "Manages login and user authentication")

Container(database, "Database", "PostgreSQL", "Stores users, projects, documents and tasks")

Container(storage, "Document Storage", "Cloud Storage", "Stores uploaded research documents")

Container(notification, "Notification Service", "Email / Messaging", "Sends alerts and updates to users")

}

Rel(student, webapp, "Uses")
Rel(supervisor, webapp, "Uses")
Rel(admin, webapp, "Uses")

Rel(webapp, api, "Calls API")

Rel(api, database, "Reads/Writes")

Rel(api, auth, "Authenticates users")

Rel(api, storage, "Stores documents")

Rel(api, notification, "Sends notifications")
```

---

# Component Diagram

```mermaid
C4Component
title Component Diagram for Backend API

Container(api, "Backend API")

Component(userService, "User Management Service", "Handles user accounts and roles")

Component(projectService, "Project Management Service", "Manages research projects")

Component(documentService, "Document Service", "Handles document uploads and version control")

Component(taskService, "Task Management Service", "Handles research task assignments")

Component(notificationService, "Notification Service", "Sends alerts and updates")

Component(authComponent, "Authentication Component", "Manages login and security")

Rel(userService, authComponent, "Uses")
Rel(projectService, userService, "Uses user data")
Rel(documentService, projectService, "Links documents to projects")
Rel(taskService, projectService, "Links tasks to projects")
Rel(notificationService, userService, "Sends messages to users")
```
