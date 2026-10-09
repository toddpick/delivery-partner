# FEAT-047 Evening delivery windows: Requirements

Status: Approved
Owner (role): Business Analyst

## Problem statement
Clients report that many recipients are out during the working day. Failed first attempts cost us a
second visit and cost the client a late delivery. We offer morning and afternoon windows only.
Add an evening window so clients can book delivery when recipients are home.

## Scope
In scope:
- A third delivery slot, `EVE` (17:00 to 21:00), selectable per parcel at booking time.
- Availability limited to postal zones where evening routes are staffed.
- Validation and a clear error when `EVE` is requested outside those zones.

Out of scope:
- Evening collection (pickup) windows.
- Per-client pricing changes; the evening window is included in the standard rate.
- Same-day booking of `EVE` after the depot cut-off.

## Business rules
1. Slots are `AM` (08:00 to 12:00), `PM` (12:00 to 17:00) and `EVE` (17:00 to 21:00).
2. All slots are expressed in depot local time, on the delivery date given in `delivery_window.date`.
3. `EVE` is available only for destination postal codes in a configured evening zone.
4. A request for `EVE` outside an evening zone is rejected; it is never silently moved to `PM`.
5. The delivery date must be today or later.

## Acceptance criteria
| # | Criterion |
|---|---|
| AC-1 | A create-parcel request with `slot: EVE` and an evening-zone postal code is accepted. |
| AC-2 | The same request with a postal code outside the evening zones is rejected with error code `slot_unavailable_for_zone`. |
| AC-3 | `AM` and `PM` behave as before for all zones. |
| AC-4 | The slot appears unchanged on `GET /v1/parcels/{parcel_id}`. |
| AC-5 | A date in the past is rejected with `delivery_date_in_past`. |

## Open questions
| # | Question | Owner (role) | Status |
|---|---|---|---|
| 1 | Add further evening zones after the first quarter? | Solution Management | Resolved: review in Q4 2026 |

## Gate G1: Requirements
- [x] Scope is clear and agreed
- [x] Business rules are complete and testable
- [x] Acceptance criteria cover each rule

| Approver (role) | Status | Date | Notes |
|---|---|---|---|
| Business Analyst | Approved | 2026-07-08 | |
| Solution Management | Approved | 2026-07-09 | Zones to be reviewed in Q4 |
