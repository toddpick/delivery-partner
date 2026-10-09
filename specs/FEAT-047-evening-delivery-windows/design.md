# FEAT-047 Evening delivery windows: Design

Status: Approved
Owner (role): Cloud Architect

## Approach
Extend the existing `delivery_window.slot` enumeration with `EVE`. Slot definitions live in
`delivery/windows.py`. Evening availability is decided by the first three characters of the
destination postal code, matched against a configured set of zone prefixes. Validation runs in
`delivery/validation.py` before a parcel is created, so no unavailable booking reaches routing.

## Interfaces
- `POST /v1/parcels`: `delivery_window.slot` now accepts `EVE`. No new fields.
- New error code `slot_unavailable_for_zone` (HTTP 422) in the existing error model.
- No change to webhooks; the slot is not part of the status payload.

## Reliability and error handling
- Validation is a pure function of the request and the zone table, so it is safe to retry.
- Zone table is loaded at start-up; a change needs a deployment. Acceptable at the current rate of change.
- If the zone table is empty, `EVE` is rejected for every parcel (fail closed).

## Data shared and retention
No new personal data is collected or shared. The postal code is already required on every parcel.

## Gate G2: Design
- [x] Integration style chosen and justified
- [x] Retries, ordering and failure behaviour defined
- [x] Error model defined

| Approver (role) | Status | Date | Notes |
|---|---|---|---|
| Cloud Architect | Approved | 2026-07-16 | |

## Gate G3: Data & governance
- [x] Data shared is listed with purpose and recipient
- [x] Personal data and retention reviewed

| Approver (role) | Status | Date | Notes |
|---|---|---|---|
| Governance (TGO) | Approved | 2026-07-21 | No new personal data |
