# Decisions

## Decision owners and gate approvers

| Gate | Name | Approver (role) | What it checks |
|---|---|---|---|
| G1 | Requirements | Business Analyst + Solution Management | Scope, business rules, acceptance criteria |
| G2 | Design | Cloud Architect | Integration style (sync API vs events/queue), reliability, error handling |
| G3 | Data & governance | Governance (TGO) | What data is shared with whom, PII, retention |
| G4 | Release sign-off | Governance (TGO) + QA Lead | Test plan, open risks accepted, final approval |

Gate status values: `Not started`, `Pending`, `Approved`, `Approved with conditions`, `Rejected`.

## Who decides what

| Topic | Owner (role) |
|---|---|
| Business rules, scope, service levels, pricing of add-ons | Solution Management |
| Acceptance criteria, field meanings, edge cases | Business Analyst |
| API style, versioning, retries, ordering, error model | Cloud Architect |
| Personal data shared, retention, third-party sharing | Governance (TGO) |
| Test plan, release readiness, acceptance of open risks | QA Lead |

## Decision log

| ID | Date | Decision | Owner (role) | Spec / section | Status |
|---|---|---|---|---|---|
| | | | | | |
