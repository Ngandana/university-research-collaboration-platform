# Class Diagram – University Research Collaboration Platform

## Introduction

This document presents a comprehensive UML class diagram for the University Research Collaboration Platform using Mermaid.js syntax. It builds upon the domain model, functional requirements (Assignment 4), use cases (Assignment 5), user stories (Assignment 6), and state/activity diagrams (Assignment 8) to produce a complete object-oriented design of the system.

---

## Class Diagram

```mermaid
classDiagram

    %% ── Enumerations ──────────────────────────────────────────
    class UserRole {
        <<enumeration>>
        STUDENT
        SUPERVISOR
        RESEARCHER
        ADMIN
    }

    class UserStatus {
        <<enumeration>>
        REGISTERED
        ACTIVE
        SUSPENDED
        DEACTIVATED
    }

    class ProjectStatus {
        <<enumeration>>
        CREATED
        ACTIVE
        COMPLETED
        CANCELLED
        ARCHIVED
    }

    class DocumentStatus {
        <<enumeration>>
        UPLOADED
        VALIDATED
        STORED
        REJECTED
        UPDATED
    }

    class TaskStatus {
        <<enumeration>>
        CREATED
        ASSIGNED
        IN_PROGRESS
        COMPLETED
        OVERDUE
    }

    class MessageStatus {
        <<enumeration>>
        COMPOSED
        SENT
        DELIVERED
        READ
    }

    class InvitationStatus {
        <<enumeration>>
        SENT
        ACCEPTED
        REJECTED
    }

    class NotificationType {
        <<enumeration>>
        TASK_UPDATE
        MESSAGE_RECEIVED
        PROJECT_UPDATE
    }

    %% ── Core Classes ──────────────────────────────────────────
    class User {
        -userId : String
        -name : String
        -email : String
        -passwordHash : String
        -role : UserRole
        -status : UserStatus
        -createdDate : Date
        +register() void
        +login() boolean
        +logout() void
        +updateProfile(name: String, email: String) void
        +deactivate() void
        +suspend() void
        +reactivate() void
        +getRole() UserRole
        +getStatus() UserStatus
    }

    class ResearchProject {
        -projectId : String
        -title : String
        -description : String
        -status : ProjectStatus
        -createdDate : Date
        -endDate : Date
        +create(title: String, desc: String) void
        +activate() void
        +complete() void
        +cancel() void
        +archive() void
        +addMember(user: User) void
        +removeMember(user: User) void
        +getStatus() ProjectStatus
        +getMembers() List~User~
    }

    class Document {
        -documentId : String
        -title : String
        -fileType : String
        -fileSize : Long
        -status : DocumentStatus
        -uploadedDate : Date
        +upload(file: File) void
        +validate() boolean
        +store() void
        +reject(reason: String) void
        +update(newFile: File) void
        +getVersionHistory() List~DocumentVersion~
        +getStatus() DocumentStatus
    }

    class DocumentVersion {
        -versionId : String
        -versionNumber : Int
        -uploadedDate : Date
        -filePath : String
        +save() void
        +retrieve() File
        +getVersionNumber() Int
    }

    class Task {
        -taskId : String
        -title : String
        -description : String
        -deadline : Date
        -status : TaskStatus
        +create(title: String, desc: String, deadline: Date) void
        +assign(user: User) void
        +start() void
        +complete() void
        +markOverdue() void
        +updateStatus(status: TaskStatus) void
        +getStatus() TaskStatus
    }

    class Message {
        -messageId : String
        -content : String
        -sentDate : DateTime
        -status : MessageStatus
        +compose(content: String) void
        +send() void
        +deliver() void
        +markRead() void
        +getStatus() MessageStatus
    }

    class Notification {
        -notificationId : String
        -message : String
        -type : NotificationType
        -isRead : Boolean
        -createdDate : DateTime
        +create(message: String, type: NotificationType) void
        +markRead() void
        +dismiss() void
        +isRead() Boolean
    }

    class Invitation {
        -invitationId : String
        -status : InvitationStatus
        -sentDate : Date
        +send() void
        +accept() void
        +reject() void
        +expire() void
        +getStatus() InvitationStatus
    }

    %% ── Relationships ─────────────────────────────────────────

    %% User uses enumerations
    User --> UserRole : role
    User --> UserStatus : status

    %% ResearchProject uses enumeration
    ResearchProject --> ProjectStatus : status

    %% Document uses enumeration
    Document --> DocumentStatus : status

    %% Task uses enumeration
    Task --> TaskStatus : status

    %% Message uses enumeration
    Message --> MessageStatus : status

    %% Invitation uses enumeration
    Invitation --> InvitationStatus : status

    %% Notification uses enumeration
    Notification --> NotificationType : type

    %% A Supervisor (User) creates ResearchProjects — association
    User "1" --> "0..*" ResearchProject : creates

    %% ResearchProject contains Documents — composition (documents depend on project)
    ResearchProject "1" *-- "0..*" Document : contains

    %% ResearchProject contains Tasks — composition
    ResearchProject "1" *-- "0..*" Task : contains

    %% Document has DocumentVersions — composition
    Document "1" *-- "1..*" DocumentVersion : has versions

    %% User uploads Documents — association
    User "1" --> "0..*" Document : uploads

    %% User uploads DocumentVersions — association
    User "1" --> "0..*" DocumentVersion : creates version

    %% Supervisor assigns Task to Student — association
    User "1" --> "0..*" Task : assigns

    %% Task is assigned to one User (Student) — association
    Task "0..*" --> "1" User : assigned to

    %% User sends Messages — association
    User "1" --> "0..*" Message : sends

    %% User receives Messages — association
    Message "0..*" --> "1" User : received by

    %% Message triggers Notification — association
    Message "1" --> "0..1" Notification : triggers

    %% Notification delivered to User — association
    Notification "0..*" --> "1" User : delivered to

    %% Invitation links Supervisor → Recipient → Project
    User "1" --> "0..*" Invitation : sends
    Invitation "0..*" --> "1" User : sent to
    Invitation "0..*" --> "1" ResearchProject : for project

    %% User membership in project (via accepted invitation)
    User "0..*" --> "0..*" ResearchProject : member of
```

---

## Key Design Decisions

### 1. Separation of User Roles via Enumeration
Rather than creating separate subclasses (`Student`, `Supervisor`, `Researcher`, `Admin`), a single `User` class with a `UserRole` enumeration was chosen. This avoids deep inheritance hierarchies and keeps the model flexible — a user's role can change without requiring a new object. This aligns with the RBAC (Role-Based Access Control) requirement from FR2 and reflects real-world identity management patterns.

### 2. Composition for Document Versioning
`DocumentVersion` is modelled as a composition within `Document`. This means a version cannot exist independently of its parent document. This design correctly captures the business rule that every document upload or update creates a traceable version record, directly supporting FR6 (Version Control).

### 3. Composition for Documents and Tasks Within Projects
Both `Document` and `Task` are composed within `ResearchProject`. Deleting or archiving a project logically makes its documents and tasks inaccessible, which reflects the business rule that archived projects are read-only.

### 4. Invitation as an Explicit Class
Instead of a direct many-to-many association between `User` and `ResearchProject`, an explicit `Invitation` class models the join process. This preserves invitation status, creation date, and lifecycle (Sent → Accepted/Rejected), satisfying FR4 (Join Project) and UC7 (Join Project use case).

### 5. Notification Decoupled from Message
`Notification` is a separate class linked to `Message` via a `triggers` association. This allows the notification system to be extended in future — for example, task deadline alerts or project status changes — without modifying the `Message` class. This aligns with the notification service identified in the Container Diagram (Assignment 3).

### 6. Enumerations for All State Fields
Every status field across entities is typed to a dedicated enumeration. This enforces valid state transitions at the type level and directly mirrors the state diagrams from Assignment 8, ensuring the class diagram and behavioural models are consistent.

### 7. Alignment With Use Cases and User Stories
Every class and key method maps to at least one use case (Assignment 5) and user story (Assignment 6):

| **Class / Method** | **Use Case** | **User Story** |
|---|---|---|
| `User.login()` | UC1: Login | US-001 |
| `ResearchProject.create()` | UC6: Create Project | US-002 |
| `Invitation.accept()` | UC7: Join Project | US-003 |
| `Document.upload()` / `validate()` | UC2: Upload Document | US-004 |
| `Task.assign()` | UC3: Assign Tasks | US-005 |
| `Task.updateStatus()` | UC4: Track Tasks | US-006 |
| `Message.send()` | UC5: Send Messages | US-007 |
| `User.deactivate()` / `reactivate()` | UC8: Manage Users | US-008 |
