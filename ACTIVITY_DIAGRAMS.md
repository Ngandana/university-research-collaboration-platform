# Activity Workflow Modeling

## Introduction

This document models system workflows using UML activity diagrams. These diagrams represent processes, decision points, and interactions between system actors.

---

# 1. User Login Workflow

```mermaid
flowchart TD
Start --> EnterCredentials
EnterCredentials --> Validate
Validate -->|Valid| AccessGranted
Validate -->|Invalid| ErrorMessage
AccessGranted --> End
ErrorMessage --> End
```

### Explanation

* Decision: Valid credentials
* Maps to:

  * FR1, US-001

---

# 2. Create Project Workflow

```mermaid
flowchart TD
Start --> EnterProjectDetails
EnterProjectDetails --> ValidateDetails
ValidateDetails -->|Valid| SaveProject
ValidateDetails -->|Invalid| Error
SaveProject --> End
Error --> End
```

---

# 3. Join Project Workflow

```mermaid
flowchart TD
Start --> ReceiveInvitation
ReceiveInvitation --> Accept?
Accept? -->|Yes| JoinProject
Accept? -->|No| Reject
JoinProject --> End
Reject --> End
```

---

# 4. Upload Document Workflow

```mermaid
flowchart TD
Start --> SelectFile
SelectFile --> ValidateFile
ValidateFile -->|Valid| UploadFile
ValidateFile -->|Invalid| RejectFile
UploadFile --> StoreFile
StoreFile --> End
RejectFile --> End
```

---

# 5. Assign Task Workflow

```mermaid
flowchart TD
Start --> CreateTask
CreateTask --> AssignUser
AssignUser --> SetDeadline
SetDeadline --> SaveTask
SaveTask --> End
```

---

# 6. Track Task Workflow

```mermaid
flowchart TD
Start --> ViewTask
ViewTask --> UpdateStatus
UpdateStatus --> SaveStatus
SaveStatus --> End
```

---

# 7. Messaging Workflow

```mermaid
flowchart TD
Start --> ComposeMessage
ComposeMessage --> SendMessage
SendMessage --> DeliverMessage
DeliverMessage --> NotifyUser
NotifyUser --> End
```

### Parallel Logic:

* Deliver + Notify happen together

---

# 8. Generate Report Workflow

```mermaid
flowchart TD
Start --> RequestReport
RequestReport --> GenerateData
GenerateData --> DisplayReport
DisplayReport --> End
```

---

## Agile Alignment

Each workflow aligns with:

* User Stories (Assignment 6)
* Sprint tasks (Assignment 6)
* Kanban tracking (Assignment 7)

This ensures continuity between design and Agile execution.
