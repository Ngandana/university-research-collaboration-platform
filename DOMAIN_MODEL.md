# Domain Model – University Research Collaboration Platform

## Introduction

This document presents the domain model for the University Research Collaboration Platform. It identifies the core entities within the system, defines their attributes and responsibilities, describes relationships between entities, and documents business rules that govern system behaviour. This model builds directly on the functional requirements (Assignment 4), use cases (Assignment 5), and Agile user stories (Assignment 6).

---

## Domain Entities

| **Entity** | **Attributes** | **Methods / Responsibilities** | **Relationships** |
|---|---|---|---|
| **User** | `userId: String`, `name: String`, `email: String`, `passwordHash: String`, `role: Enum(Student, Supervisor, Researcher, Admin)`, `status: Enum(Registered, Active, Suspended, Deactivated)` | `register()`, `login()`, `logout()`, `updateProfile()`, `deactivate()` | Creates/joins Projects; sends Messages; assigned Tasks; sends/receives Invitations |
| **ResearchProject** | `projectId: String`, `title: String`, `description: String`, `status: Enum(Created, Active, Completed, Cancelled, Archived)`, `createdDate: Date`, `endDate: Date` | `create()`, `activate()`, `archive()`, `cancel()`, `addMember()`, `removeMember()` | Owned by Supervisor (User); has many Members (Users); contains Documents and Tasks |
| **Document** | `documentId: String`, `title: String`, `fileType: String`, `fileSize: Long`, `status: Enum(Uploaded, Validated, Stored, Rejected, Updated)`, `uploadedDate: Date` | `upload()`, `validate()`, `store()`, `reject()`, `getVersionHistory()` | Belongs to a ResearchProject; uploaded by a User; has many DocumentVersions |
| **DocumentVersion** | `versionId: String`, `versionNumber: Int`, `uploadedDate: Date`, `filePath: String` | `save()`, `retrieve()` | Belongs to a Document; uploaded by a User |
| **Task** | `taskId: String`, `title: String`, `description: String`, `deadline: Date`, `status: Enum(Created, Assigned, InProgress, Completed, Overdue)` | `create()`, `assign()`, `start()`, `complete()`, `markOverdue()` | Belongs to a ResearchProject; assigned to a User (Student); created by a User (Supervisor) |
| **Message** | `messageId: String`, `content: String`, `sentDate: DateTime`, `status: Enum(Composed, Sent, Delivered, Read)` | `send()`, `deliver()`, `markRead()` | Sent by a User; received by a User; triggers a Notification |
| **Notification** | `notificationId: String`, `message: String`, `type: Enum(TaskUpdate, MessageReceived, ProjectUpdate)`, `isRead: Boolean`, `createdDate: DateTime` | `create()`, `markRead()`, `dismiss()` | Sent to a User; triggered by a Message or Task event |
| **Invitation** | `invitationId: String`, `status: Enum(Sent, Accepted, Rejected)`, `sentDate: Date` | `send()`, `accept()`, `reject()`, `expire()` | Sent by a User (Supervisor) to another User; linked to a ResearchProject |

---

## Relationships Between Entities

- A **User** with the role of *Supervisor* **creates** one or more **ResearchProjects** (1 to many).
- A **ResearchProject** **has** one or more **Users** as members via **Invitations** (many to many through Invitation).
- A **ResearchProject** **contains** zero or more **Documents** (1 to many).
- A **Document** **has** one or more **DocumentVersions** (1 to many, composition).
- A **ResearchProject** **contains** zero or more **Tasks** (1 to many).
- A **Task** is **assigned to** exactly one **User** (0..1 to 1).
- A **User** **sends** zero or more **Messages** to other Users (1 to many).
- A **Message** **triggers** zero or one **Notification** (1 to 0..1).
- A **Notification** is **received by** exactly one **User** (1 to 1).
- An **Invitation** is **sent by** one User and **directed to** one User, linked to one ResearchProject.

---

## Business Rules

1. A **User** must verify their email before their account becomes Active.
2. Only a **Supervisor** or **Researcher** may create a **ResearchProject**.
3. A **Student** may only join a project by accepting a valid **Invitation**; they cannot join without one.
4. A **Document** must pass file-type and file-size validation before it is stored; rejected documents are not persisted.
5. Only **PDF** and **DOCX** file formats are permitted for document uploads.
6. Every time a **Document** is updated, a new **DocumentVersion** record is created; previous versions are retained.
7. Only a **Supervisor** may create and assign **Tasks** within a project.
8. A **Task** is automatically marked **Overdue** if its deadline passes without the status being set to Completed.
9. A **Message** triggers a **Notification** to the recipient upon successful delivery.
10. An **Administrator** may suspend or deactivate any **User** account; only an Administrator may reactivate a suspended account.
11. A **ResearchProject** moves to **Archived** status after it is either Completed or Cancelled; archived projects are read-only.
