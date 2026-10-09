# Status webhooks

We send an HTTP `POST` to the client's webhook URL whenever a parcel changes status.

## Delivery guarantees
- **At-least-once.** The same event can be delivered more than once. De-duplicate on `event_id`.
- **May arrive out of order.** Events for one parcel can arrive in a different order than they occurred.
  Use `occurred_at` to decide which event is newer; do not rely on arrival order.
- **Retries for 24 hours.** Any response other than `2xx` (or no response within 10 seconds) is retried
  with increasing delays (1 min, 5 min, 15 min, then hourly) until 24 hours after the first attempt.
  After that the event is dropped; the current state is always available from `GET /v1/parcels/{parcel_id}`.

## Request

Headers:

| Header | Value |
|---|---|
| `Content-Type` | `application/json` |
| `X-Delivery-Event-Id` | Same as `event_id` in the body |
| `X-Delivery-Signature` | `sha256=` followed by the hex HMAC-SHA256 of the raw request body |

The HMAC key is the client's webhook secret, issued at onboarding.

Body:

```json
{
  "event_id": "evt_01J8Z3K5Q2",
  "event_type": "parcel.status_changed",
  "parcel_id": "DP-7Q4K2M9X",
  "client_reference": "A-10482",
  "status": "OUT_FOR_DELIVERY",
  "occurred_at": "2026-09-14T09:41:12"
}
```

All timestamps are ISO-8601 in UTC.

When `status` is `DELIVERED` the body also contains `proof_of_delivery` (see `docs/data-dictionary.md`).

## Verifying the signature
Compute HMAC-SHA256 over the raw bytes of the body with your webhook secret and compare with the
header value using a constant-time comparison. Reject the request with `401` on mismatch.

## Expected response
Return `200` to `204` as soon as the event is stored. Do heavy work asynchronously.

## Status codes sent
`CREATED`, `LABELLED`, `COLLECTED`, `AT_DEPOT`, `HELD_AT_DEPOT`, `OUT_FOR_DELIVERY`, `DELIVERED`,
`FAILED_ATTEMPT`, `RETURNED_TO_SENDER`.
