# Specifications

This team uses spec-driven development. Every feature or integration gets a folder here with three
documents, written in order, and four approval gates.

## Process

1. **Requirements** (`requirements.md`): problem, scope, business rules, acceptance criteria.
2. **Design** (`design.md`): approach, interfaces, reliability and error handling, data shared.
3. **Tasks** (`tasks.md`): the implementation and test work, traceable to requirements.

Start a new spec by copying `_templates/` into `specs/<ID>-<short-name>/`. Set `Status` at the top of
each document: `Draft`, `In review`, `Approved`.

## Gates

| Gate | Name | Approver (role) | What it checks |
|---|---|---|---|
| G1 | Requirements | Business Analyst + Solution Management | Scope, business rules, acceptance criteria |
| G2 | Design | Cloud Architect | Integration style (sync API vs events/queue), reliability, error handling |
| G3 | Data & governance | Governance (TGO) | What data is shared with whom, PII, retention |
| G4 | Release sign-off | Governance (TGO) + QA Lead | Test plan, open risks accepted, final approval |

Gate status values: `Not started`, `Pending`, `Approved`, `Approved with conditions`, `Rejected`.

Gates are taken in order. A gate is requested when its document is complete enough to review.

## Open items

Items or risks that cannot be resolved yet are recorded as `Open — owner: <role>`. They do not block
drafting, but G4 requires each one to be either resolved or explicitly accepted by the approvers.

## Specs

| Folder | Status |
|---|---|
| `FEAT-047-evening-delivery-windows/` | Approved, released |
| `INT-310-orders-client-onboarding/` | Draft |
