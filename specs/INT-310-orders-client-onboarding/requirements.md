# INT-310 Orders client onboarding: Requirements

Status: Draft
Owner (role): Business Analyst

## Problem statement
Onboard a new retail client that will book parcels via our API and receive status updates.

## Scope
In scope:
- Booking parcels through `POST /v1/parcels`.
- Receiving status updates through webhooks.

Out of scope:
- To be agreed.

## Business rules (Delivery side, known)
1. One parcel represents one physical box. A client with a multi-box order books one parcel per box.
2. Hazardous goods are not accepted (terms of service). The API rejects `dangerous_goods: true`.
3. A recipient phone number is required on every parcel; it is used for SMS delivery notifications.
4. Maximum parcel weight is 30.00 kg.
5. `client_reference` is optional, at most 12 characters, and is echoed back on every webhook.
6. Delivery windows are `AM`, `PM` and `EVE` in depot local time; `EVE` is limited to some postal zones.
7. Proof of delivery is a photo by default. Signature is a paid add-on (`signature_service`).
8. A parcel can be cancelled only before it reaches `COLLECTED`.
9. API and webhooks only; there is no message-bus or queue integration.

## Field mapping
_To be completed with the client's side._

## Status mapping
_To be completed with the client's side._

## Acceptance criteria
_To be completed._

## Open questions
| # | Question | Owner (role) | Status |
|---|---|---|---|
| | | | |

## Gate G1: Requirements
- [ ] Scope is clear and agreed
- [ ] Business rules are complete and testable
- [ ] Acceptance criteria cover each rule

| Approver (role) | Status | Date | Notes |
|---|---|---|---|
| Business Analyst | Pending | | |
| Solution Management | Pending | | |
