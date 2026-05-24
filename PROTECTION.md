# Branch Protection Rules — University Research Collaboration Platform

## What Rules Are Applied to `main`

The following branch protection rules are configured on the `main` branch via
**GitHub → Settings → Branches → Branch protection rules**:

| Rule | Setting |
|---|---|
| Require pull request before merging | ✅ Enabled |
| Required number of approvals | 1 reviewer |
| Require status checks to pass | ✅ Enabled (`Run Tests` job) |
| Require branches to be up to date | ✅ Enabled |
| Block direct pushes to `main` | ✅ Enabled |
| Include administrators | ✅ Enabled |

---

## Why These Rules Matter

### 1. Require Pull Request Reviews
No developer — including the repository owner — can push code directly to `main`.
Every change must go through a Pull Request and receive at least one approval from
a reviewer before it can be merged.

**Why this matters:** A second pair of eyes catches bugs, logic errors, and security
issues that the original developer missed. In a group project, it also ensures all
team members are aware of changes being made to the codebase.

### 2. Require Status Checks to Pass (CI)
The GitHub Actions `Run Tests` job must complete successfully before a PR can be
merged. If any of the 249 tests fail, the merge button is blocked automatically.

**Why this matters:** This guarantees that broken code can never reach `main`. The
`main` branch is always in a deployable state. No manual "did you run the tests?"
conversation is needed — the pipeline enforces it.

### 3. Require Branches to Be Up to Date
Before merging, the PR branch must incorporate the latest changes from `main`. This
prevents a scenario where two developers merge conflicting changes without realising
it.

**Why this matters:** It eliminates a common class of integration bugs where code
works on a feature branch but breaks when combined with concurrent changes from
teammates.

### 4. Block Direct Pushes
Even administrators cannot bypass the PR + review + CI requirement. All changes
go through the same process regardless of seniority.

**Why this matters:** It removes the temptation to "quickly push a small fix" directly
to `main` without review or testing — which is how most production incidents start.

### 5. Include Administrators
The rules apply to everyone, including the repository owner.

**Why this matters:** Consistency. A rule that can be bypassed by some people
is not a rule — it is a suggestion. Applying it to all contributors ensures the
protection is meaningful.

---

## How the CI/CD Pipeline Enforces This

```
Developer pushes to feature branch
        ↓
GitHub Actions runs all 249 tests automatically
        ↓
Developer opens a Pull Request to main
        ↓
CI must pass ──── if FAIL → merge blocked ❌
        ↓
1 reviewer must approve ──── if not approved → merge blocked ❌
        ↓
PR merged to main ✅
        ↓
CD pipeline runs → builds Python wheel artifact → uploaded to GitHub Actions
```

---

## Industry Relevance

These rules reflect standard practices used at software companies of all sizes.
The Git Flow and Trunk-Based Development models both rely on protected main branches
with automated CI gates. GitHub's own internal engineering guidelines, Google's
engineering practices documentation, and Microsoft's Developer Division all mandate
equivalent protections on production branches.

For this project, the rules ensure that every version of the platform that reaches
`main` has passed all unit tests, integration tests, and API tests — giving confidence
to both the development team and any future users of the platform.
