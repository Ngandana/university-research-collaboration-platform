# Test Cases (Advanced)

## Functional Test Cases

| Test Case ID | Req ID | Description         | Steps                   | Expected Result | Status |
| ------------ | ------ | ------------------- | ----------------------- | --------------- | ------ |
| TC-001       | FR1    | Login success       | Enter valid credentials | Access granted  | TBD    |
| TC-002       | FR1    | Login failure       | Enter wrong password    | Error displayed | TBD    |
| TC-003       | FR3    | Create project      | Submit valid data       | Project created | TBD    |
| TC-004       | FR5    | Upload valid file   | Upload PDF              | File stored     | TBD    |
| TC-005       | FR5    | Upload invalid file | Upload .exe             | Rejected        | TBD    |
| TC-006       | FR7    | Assign task         | Assign valid user       | Task assigned   | TBD    |
| TC-007       | FR8    | Update task         | Change status           | Status updated  | TBD    |
| TC-008       | FR9    | Send message        | Send message            | Delivered       | TBD    |
| TC-009       | FR6    | Version control     | Upload new version      | Version saved   | TBD    |

---

## Edge Case Testing

| Test Case ID | Description            | Expected Result                |
| ------------ | ---------------------- | ------------------------------ |
| TC-010       | Upload very large file | System rejects                 |
| TC-011       | Concurrent uploads     | No data loss                   |
| TC-012       | Multiple users editing | Version consistency maintained |

---

## Non-Functional Tests

### Performance Test

* Simulate 1000 concurrent users
* Expected: ≤ 2 seconds response

### Security Test

* Attempt SQL injection
* Expected: Input sanitized

### Scalability Test

* Increase users to 5000
* Expected: System scales without crash
