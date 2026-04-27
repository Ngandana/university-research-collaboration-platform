# Reflection – Assignment 9: Domain Modeling and Class Diagram Development

## Introduction

This reflection critically examines the process of designing the domain model and class diagram for the University Research Collaboration Platform. It covers the challenges encountered, the alignment of this work with previous assignments, the trade-offs made, and the lessons learned about object-oriented design.

---

## 1. Challenges in Designing the Domain Model and Class Diagram

### Abstraction and Entity Identification

One of the most significant challenges in designing the domain model was determining the correct level of abstraction for each entity. The system encompasses a wide range of concepts — users, projects, documents, tasks, messages, notifications, and invitations — and the initial difficulty was deciding which concepts warranted their own dedicated entity and which could be absorbed as attributes of another.

For example, the decision around `DocumentVersion` required careful thought. A simpler approach would have been to store version information as a list of metadata attributes directly on `Document`. However, this would have obscured the lifecycle and individual traceability of each version, which is a core business requirement (FR6). Creating `DocumentVersion` as a distinct entity, composed within `Document`, better models the real-world concept and allows future extension, such as adding a reviewer or approval status to a specific version.

Similarly, `Invitation` could have been modelled as a simple boolean flag or a list attribute on `ResearchProject`. However, the invitation has its own lifecycle — it can be sent, accepted, rejected, or expire — which warrants a first-class entity. This realisation came from revisiting the state diagrams from Assignment 8, where the Invitation State Diagram clearly showed that this object carries meaningful state independently.

### Defining Relationships and Multiplicity

Defining relationships and their multiplicities was another area of difficulty. The relationship between `User` and `ResearchProject` is inherently many-to-many — a project has many members, and a user can belong to many projects. However, modelling this as a raw many-to-many association would lose the invitation context. Introducing `Invitation` as an associative entity resolved this and added semantic meaning to the join.

Task assignment presented a similar challenge. A task is assigned by a Supervisor to a Student, but both are of type `User`. This required two associations on `Task`: one representing who created/assigned it (the Supervisor) and one representing who it is assigned to (the Student). Representing this clearly in the class diagram without making it appear circular required careful use of navigability and association labels.

### Method Definitions

Identifying meaningful and correctly scoped methods for each class was initially difficult. There was a tendency to either include too many low-level utility methods (e.g., `getFilePath()`, `setVersionNumber()`) or too few, leaving classes with insufficient behavioural definition. The resolution was to anchor methods to the business operations identified in the use case specifications from Assignment 5. Every method in the class diagram corresponds to a step in a basic or alternative use case flow, ensuring that methods represent genuine system responsibilities rather than arbitrary getters and setters.

---

## 2. Alignment With Previous Assignments

### Requirements (Assignment 4)

Each class in the diagram maps to one or more functional requirements. The `User` class addresses FR1 (Authentication) and FR2 (Role-Based Access Control). `ResearchProject` addresses FR3 (Create Project) and FR4 (Join Project). `Document` and `DocumentVersion` together address FR5 (Document Upload) and FR6 (Version Control). `Task` addresses FR7 (Task Assignment) and FR8 (Task Tracking). `Message` and `Notification` together address FR9 (Messaging and Notifications). This direct traceability ensures that the class diagram is grounded in documented system requirements rather than speculative design.

### Use Cases (Assignment 5)

The use case specifications from Assignment 5 directly informed method signatures. For instance, UC2 (Upload Document) specifies a flow that includes selecting a file, validating it, and storing it. This maps to `Document.upload()`, `Document.validate()`, and `Document.store()` as distinct methods, each representing a meaningful step in the workflow. The alternative flow — where an invalid file is rejected — is captured by `Document.reject()`. This level of traceability between use case steps and class methods is a hallmark of rigorous object-oriented analysis.

### State Diagrams (Assignment 8)

The state diagrams from Assignment 8 had a direct and significant influence on the class diagram. Every status enumeration (`UserStatus`, `ProjectStatus`, `DocumentStatus`, `TaskStatus`, `MessageStatus`, `InvitationStatus`) was derived directly from the states identified in those diagrams. The transitions in the state diagrams informed the methods: for example, the transition from `Assigned` to `InProgress` in the Task State Diagram corresponds to `Task.start()`, and the transition to `Overdue` corresponds to `Task.markOverdue()`. This consistency ensures that the static structure defined in the class diagram is fully compatible with the dynamic behaviour modelled previously.

### Activity Diagrams (Assignment 8)

The activity diagrams also contributed by clarifying decision points and parallel processes. The Login workflow confirmed that `User.login()` should return a boolean (success or failure) rather than void. The Upload Document workflow clarified that validation is a separate step from storage, justifying the separation of `validate()` and `store()` as distinct methods rather than a single `upload()` operation.

---

## 3. Trade-offs Made

### Inheritance Versus Role-Based Design

A natural object-oriented instinct would be to model `Student`, `Supervisor`, `Researcher`, and `Admin` as subclasses of `User`, with each inheriting common attributes and overriding role-specific behaviour. This approach was deliberately avoided in favour of a single `User` class with a `UserRole` enumeration. The key trade-off here is between type safety and flexibility. Inheritance would make role-specific constraints enforceable at the type level (e.g., only a `Supervisor` can call `createProject()`), but it would make it impossible for a user's role to change at runtime without creating a new object. In a real university system, a researcher might also supervise students, and a user's permissions evolve. The role-enumeration approach prioritises runtime flexibility and simpler object management, with access control enforced at the application or service layer rather than the class hierarchy.

### Composition Versus Aggregation

Documents and Tasks are modelled as compositions within `ResearchProject`, meaning they cannot logically exist outside of a project. This is a deliberate design choice that reflects the business rule that archived projects are read-only and that tasks and documents have no meaning without a project context. The trade-off is that this makes independent reuse of documents across multiple projects impossible within the model. A more flexible design might model documents as aggregates — shared resources that projects reference — but this would introduce complexity around access control and version history that is beyond the current system scope.

### Simplifying the Notification System

The `Notification` class was kept intentionally simple. In a production system, notifications would likely be typed further — task notifications, message notifications, project notifications — potentially as subclasses or separate entities. For the scope of this assignment, a `NotificationType` enumeration on a single `Notification` class achieves the necessary distinction without over-engineering the model. This keeps the diagram readable while preserving the ability to extend the design in future.

---

## 4. Lessons Learned About Object-Oriented Design

This assignment reinforced several important principles of object-oriented design. First, the value of traceability cannot be overstated. Every design decision — which entities to include, which relationships to define, which methods to expose — was easier to justify and more academically defensible when it could be traced back to a documented requirement, use case, or behavioural model. This is not merely an academic exercise; traceability is essential in professional software engineering to manage change, support testing, and communicate design intent.

Second, the process of moving from a domain model to a class diagram revealed that the two artefacts serve different purposes. The domain model captures the vocabulary and business rules of the problem domain in a readable, stakeholder-accessible form. The class diagram refines this into a technical specification that a developer could implement. Both are necessary, and neither can substitute for the other.

Third, the challenge of defining method boundaries highlighted the importance of the Single Responsibility Principle. Methods that do too much — such as a single `uploadDocument()` that validates, stores, and versions in one operation — are harder to test, harder to change, and harder to trace to specific requirements. Breaking these into `validate()`, `store()`, and the version-creation logic within `DocumentVersion.save()` produces a more maintainable and testable design.

Finally, this assignment demonstrated that good object-oriented design is iterative. The first draft of the class diagram contained redundancies, unclear multiplicities, and methods that did not align with the use case flows. Refining the diagram through comparison with the domain model, state diagrams, and use case specifications produced a significantly stronger result. This iterative refinement process mirrors real-world software design practice, where designs evolve through review and validation rather than being finalised in a single pass.
