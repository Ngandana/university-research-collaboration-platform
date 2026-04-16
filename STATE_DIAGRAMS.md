# Object State Modeling

## Introduction

This document models the lifecycle of key system objects using UML state transition diagrams. These diagrams illustrate how objects change states in response to events and align with system requirements and use cases.

---

# 1. User Account State Diagram

```mermaid
stateDiagram-v2
[*] --> Registered
Registered --> Active : Verify Email
Active --> Suspended : Violation
Suspended --> Active : Admin Reactivates
Active --> Deactivated : User Deletes Account
Deactivated --> [*]
```

### Explanation

* **States:** Registered, Active, Suspended, Deactivated
* **Key Transition:** Email verification activates account
* **Mapping:**

  * FR1: User Login
  * US-001: Login functionality

---

# 2. Research Project State Diagram

```mermaid
stateDiagram-v2
[*] --> Created
Created --> Active : Supervisor Starts Project
Active --> Completed : Project Finished
Active --> Cancelled : Supervisor Cancels
Completed --> Archived
Cancelled --> Archived
Archived --> [*]
```

### Explanation

* Reflects project lifecycle
* Maps to:

  * FR3: Create Project
  * US-002

---

# 3. Document State Diagram

```mermaid
stateDiagram-v2
[*] --> Uploaded
Uploaded --> Validated : System Validates
Validated --> Stored : Saved Successfully
Validated --> Rejected : Invalid File
Stored --> Updated : New Version Uploaded
Updated --> Stored
```

### Explanation

* Includes validation (important for backend logic)
* Maps to:

  * FR5: Upload Document
  * US-004

---

# 4. Task State Diagram

```mermaid
stateDiagram-v2
[*] --> Created
Created --> Assigned : Supervisor Assigns
Assigned --> InProgress : Student Starts
InProgress --> Completed : Task Done
InProgress --> Overdue : Deadline Passed
Overdue --> Completed
```

### Explanation

* Shows task tracking lifecycle
* Maps to:

  * FR7, FR8
  * US-005, US-006

---

# 5. Message State Diagram

```mermaid
stateDiagram-v2
[*] --> Composed
Composed --> Sent
Sent --> Delivered
Delivered --> Read
```

### Explanation

* Messaging workflow
* Maps to:

  * FR9
  * US-007

---

# 6. User Invitation State Diagram

```mermaid
stateDiagram-v2
[*] --> Sent
Sent --> Accepted
Sent --> Rejected
Accepted --> JoinedProject
Rejected --> [*]
JoinedProject --> [*]
```

### Explanation

* Handles joining projects
* Maps to:

  * FR4
  * US-003

---

# 7. Report State Diagram

```mermaid
stateDiagram-v2
[*] --> Requested
Requested --> Generated
Generated --> Viewed
Viewed --> Archived
```

### Explanation

* Reporting lifecycle
* Maps to:

  * FR10
  * US-009
