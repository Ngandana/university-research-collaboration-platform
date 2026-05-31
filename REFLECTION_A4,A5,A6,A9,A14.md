# Assignment 4 Reflection

## Challenges Faced in Balancing Stakeholder Needs

One of the main challenges encountered during this assignment was balancing the different needs and priorities of various stakeholders. Each stakeholder group had unique expectations from the system, which sometimes conflicted with one another.

For example, students required a simple and user-friendly interface, while IT support staff prioritized system maintainability and technical robustness. Similarly, supervisors needed detailed tracking and reporting features, which could increase system complexity and impact usability.

Another challenge was addressing security requirements while maintaining ease of access. Implementing strong authentication mechanisms can sometimes reduce user convenience, requiring careful design decisions to balance security and usability.

Scalability was also a key consideration, as the system must support a growing number of users and research projects. Designing for scalability required making assumptions about future system usage while ensuring the system remains efficient and cost-effective.

Overall, this assignment highlighted the importance of requirement prioritization, stakeholder communication, and making informed trade-offs when designing complex systems.


## Additional Reflection: Agile Tools and Kanban Implementation

Another challenge encountered in this assignment was transitioning from theoretical Agile concepts to practical implementation using GitHub tools. While user stories and sprint planning were previously defined conceptually, implementing them within GitHub Projects required a deeper understanding of how Agile workflows are supported in real-world environments.

Setting up the Kanban board and customizing it to reflect the system’s workflow was particularly challenging. Deciding which columns to include, such as "Testing" and "Blocked", required careful consideration to ensure the board accurately represented the development process without becoming overly complex.

Additionally, linking user stories (issues), labels, and milestones introduced the challenge of maintaining consistency and traceability. Each issue needed to correctly reflect its priority, requirement, and role within the sprint, which required attention to detail.

Another key learning point was understanding the value of visualization in Agile development. The Kanban board provided a clear overview of task progress, making it easier to identify bottlenecks and manage workload effectively.

Overall, this part of the assignment demonstrated the importance of integrating Agile tools into the development process and highlighted how platforms like GitHub can support structured and efficient project management.


# Assignment 5 Reflection (Advanced)

## Challenges in Translating Requirements into Use Cases and Test Cases

A major challenge in this assignment was ensuring alignment between stakeholder needs, functional requirements, and system behavior. While requirements describe system capabilities, use cases required translating these into realistic user interactions.

One key difficulty was handling conflicting stakeholder needs. For example, students require a simple and intuitive interface, while IT staff prioritize system security and robustness. Balancing usability and security required careful abstraction in use case modeling.

Another challenge was identifying appropriate system boundaries. It was necessary to determine which processes belong within the system and which are external, particularly for authentication and notifications.

Developing alternative flows required anticipating real-world failures such as invalid inputs, system errors, and concurrency issues. This highlighted the complexity of designing reliable systems beyond ideal scenarios.

Test case development introduced the need for measurable validation. Ensuring that each test case directly mapped to a requirement required the use of a traceability matrix, which improved consistency and completeness.

Additionally, non-functional requirements such as performance and scalability were more difficult to validate compared to functional requirements. Designing realistic performance tests required assumptions about system load and usage patterns.

Overall, this assignment emphasized the importance of traceability, validation, and systematic thinking in software engineering. It demonstrated how structured modeling techniques such as use cases and test cases ensure that systems meet stakeholder expectations and operate reliably in real-world environments.


# Assignment 6 Reflection

## Challenges in Agile Planning and Prioritization

One of the key challenges in this assignment was prioritizing user stories effectively while balancing different system requirements. As the sole decision-maker in this simulated Agile environment, it was difficult to objectively determine which features should be implemented first without real stakeholder input.

Another challenge was breaking down large system requirements into smaller, manageable user stories. Some functionalities, such as document management and task tracking, were initially too broad and had to be refined to meet the INVEST criteria. Ensuring that each story was independent and testable required careful analysis.

Effort estimation also presented challenges. Assigning story points required making assumptions about complexity, development time, and dependencies. Without practical implementation experience, it was difficult to ensure accurate estimations, which reflects a common challenge in real Agile projects.

Additionally, aligning Agile practices with previously defined system requirements required maintaining traceability. Each user story needed to clearly map back to functional requirements and use cases, ensuring consistency across all assignments.

Balancing technical requirements (such as security and scalability) with user-focused features was another difficulty. For example, implementing encryption is essential but does not directly deliver visible value to end users, making prioritization more complex.

Overall, this assignment highlighted the importance of iterative planning, prioritization, and adaptability in Agile development. It demonstrated how Agile methodologies help manage complexity while ensuring that the system delivers value incrementally.


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

# Reflection — Assignment 14: Peer Review and Open-Source Collaboration

## Introduction

This reflection examines the process of preparing the University Research Collaboration Platform for open-source collaboration, the challenges encountered when thinking about onboarding external contributors, and the broader lessons learned about how open-source projects function in practice.

---

## How I Improved the Repository Based on Peer Feedback

Before preparing the repository for peer review, the project was technically complete — 249 tests passing, a working REST API, CI/CD pipeline, and full documentation of the domain model and architecture. However, being technically complete and being ready for collaboration are two different things entirely.

The process of writing `CONTRIBUTING.md` forced me to look at the project through the eyes of someone seeing it for the first time. I realised that while I understood how every piece connected — from the domain model through the repository layer to the service layer and API — none of that context was visible to an outsider. A new contributor landing on the repository would see a collection of folders without understanding why the layers exist or how they relate to each other.

Based on this realisation, I improved the README significantly, adding a "Getting Started" section with step-by-step setup instructions, a project structure overview, and a table mapping each folder to its responsibility. I also updated the `CONTRIBUTING.md` to include not just the mechanical steps of forking and submitting a PR, but also the reasoning behind the coding standards — why type hints are required, why docstrings matter, and why tests must cover new code.

The peer review process itself reinforced the importance of documentation. Repositories that received more engagement from classmates were consistently those with clearer setup instructions and more descriptive issue labels. This validated the investment in `CONTRIBUTING.md`, `ROADMAP.md`, and the labelling of issues as `good-first-issue` or `feature-request`.

---

## Challenges in Onboarding Contributors

The most significant challenge in preparing for external contributors was achieving the right level of abstraction in the contribution guidelines. Too much detail and the document becomes overwhelming; too little and contributors are left guessing. Finding that balance required thinking carefully about what prior knowledge could be assumed — for example, assuming familiarity with Git and Python, but not with the Repository Pattern or the specific business rules of the platform.

A second challenge was issue labelling. The `good-first-issue` label is meant to signal tasks that are self-contained and achievable without deep knowledge of the codebase. However, looking at the existing issues, many of them required understanding multiple layers of the system — the domain model, the service layer, and the API — before a meaningful contribution could be made. This led to the creation of more granular issues focused on specific, isolated additions like adding a single new endpoint or writing a Postman collection, which are genuinely approachable for a first-time contributor.

A third challenge was dependency management. The project uses a virtual environment, and the setup instructions needed to be tested from scratch to ensure they actually worked on a fresh machine. This exercise revealed that the `requirements.txt` file was missing from the repository until Assignment 13, which would have blocked any contributor from getting started.

---

## Lessons Learned About Open-Source Collaboration

The most important lesson from this assignment is that open-source readiness is a continuous process, not a final state. Every feature added, every test written, and every architectural decision made creates work for the documentation and contribution infrastructure. Projects that treat documentation as an afterthought accumulate what might be called "documentation debt" — the gap between what the code does and what outsiders can understand about it grows over time until the project becomes effectively inaccessible to new contributors.

A second lesson is that the quality of issues is as important as the quality of code. GitHub stars and forks are signals of perceived value, but what drives actual contributions is the clarity and approachability of open issues. A repository with fifty vague issues will attract fewer contributors than one with ten well-described, labelled, and scoped issues with clear acceptance criteria.

Finally, this assignment illustrated the relationship between automated testing and open-source confidence. The CI/CD pipeline, particularly the requirement that all 249 tests pass before any PR can be merged, serves a dual purpose: it protects the codebase from regressions, and it signals to potential contributors that the project is maintained to a professional standard. A contributor who sees a green pipeline on every commit gains confidence that their own contributions will be validated fairly and objectively, without depending on a maintainer manually checking their work.

These lessons extend beyond academic projects. The practices established here — branch protection, automated testing, clear documentation, labelled issues, and a public roadmap — are the same practices that make successful open-source projects like FastAPI, pytest, and Django welcoming to contributors at all experience levels.

