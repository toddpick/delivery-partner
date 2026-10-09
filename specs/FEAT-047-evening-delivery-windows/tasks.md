# FEAT-047 Evening delivery windows: Tasks

Status: Approved

## Tasks
| # | Task | Covers | Owner | Status |
|---|---|---|---|---|
| 1 | Add `EVE` to the slot enumeration and slot table | Rule 1 | Backend | Done |
| 2 | Evening zone prefix table and `evening_available()` | Rule 3 | Backend | Done |
| 3 | Validation: zone check and past-date check | Rules 4, 5 | Backend | Done |
| 4 | Update OpenAPI and data dictionary | AC-1, AC-4 | Backend | Done |
| 5 | Unit tests for windows and validation | AC-1 to AC-5 | Backend | Done |
| 6 | Routing team briefed on evening routes | Rule 3 | Operations | Done |

## Test plan
- Unit tests in `tests/test_windows.py` and `tests/test_validation.py` cover AC-1 to AC-3 and AC-5.
- Manual check in the staging environment for AC-4 with one parcel per slot.

## Risks and open items
| # | Item | Owner (role) | Status |
|---|---|---|---|
| 1 | Evening zone coverage is small at launch | Solution Management | Accepted by G4 approvers |

## Gate G4: Release sign-off
- [x] Test plan executed
- [x] Open risks resolved or explicitly accepted
- [x] Ready for release

| Approver (role) | Status | Date | Notes |
|---|---|---|---|
| Governance (TGO) | Approved | 2026-08-12 | |
| QA Lead | Approved | 2026-08-11 | Staging run clean |
