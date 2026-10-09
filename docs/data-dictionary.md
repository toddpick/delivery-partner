# Data dictionary

## Parcel (create request)

| Field | Type | Required | Units / format | Notes |
|---|---|---|---|---|
| `client_reference` | string | no | max 12 characters | Echoed back on every webhook |
| `recipient.name` | string | yes | | |
| `recipient.phone` | string | yes | E.164, e.g. `+15550100123` | Used for SMS delivery notifications |
| `address.street1` | string | yes | | |
| `address.street2` | string | no | | |
| `address.city` | string | yes | | |
| `address.region` | string | yes | | State or province code |
| `address.postal_code` | string | yes | | |
| `address.country_code` | string | yes | ISO 3166-1 alpha-2 | |
| `weight_kg` | decimal | yes | kilograms, 2 decimal places, max 30.00 | |
| `dimensions_cm.length` / `width` / `height` | integer | yes | centimetres | |
| `special_handling` | boolean | no | default `false` | When true the driver is told "handle with care" |
| `dangerous_goods` | boolean | no | must be `false` or omitted | Hazardous goods are not accepted (terms of service); `true` is rejected |
| `delivery_window.date` | string | yes | `YYYY-MM-DD`, depot local date | |
| `delivery_window.slot` | enum | yes | `AM`, `PM`, `EVE` | Times are depot local time |
| `signature_service` | boolean | no | default `false` | Paid add-on, extra fee per parcel. Default proof is a photo |

One parcel is one physical box.

## Parcel (response)

| Field | Type | Notes |
|---|---|---|
| `parcel_id` | string | `DP-` followed by 8 uppercase alphanumerics, e.g. `DP-7Q4K2M9X` |
| `status` | enum | See status codes |
| `created_at` | string | ISO-8601, UTC |
| `proof_of_delivery` | object | Present once `DELIVERED` |

## Delivery windows

| Slot | Local time | Availability |
|---|---|---|
| `AM` | 08:00 to 12:00 | All zones |
| `PM` | 12:00 to 17:00 | All zones |
| `EVE` | 17:00 to 21:00 | Evening zones only (FEAT-047) |

## Proof of delivery

| Field | Type | Notes |
|---|---|---|
| `type` | enum | `PHOTO` (default) or `SIGNATURE` (when `signature_service` is true) |
| `photo_url` | string | Present for `PHOTO` |
| `signed_by` | string | Present for `SIGNATURE` |
| `captured_at` | string | ISO-8601, UTC |

## Status codes

| Code | Meaning |
|---|---|
| `CREATED` | Parcel booked |
| `LABELLED` | Label generated |
| `COLLECTED` | Picked up from the client; cancellation no longer possible |
| `AT_DEPOT` | Arrived at the delivery depot |
| `HELD_AT_DEPOT` | Kept at the depot (for example awaiting a corrected address) |
| `OUT_FOR_DELIVERY` | With the driver |
| `DELIVERED` | Delivered; proof of delivery attached |
| `FAILED_ATTEMPT` | Delivery attempted, recipient not reached |
| `RETURNED_TO_SENDER` | Returned to the client |

## Webhook event

| Field | Type | Notes |
|---|---|---|
| `event_id` | string | Unique per event; use for de-duplication |
| `event_type` | string | `parcel.status_changed` |
| `parcel_id` | string | |
| `client_reference` | string or null | |
| `status` | enum | Status code |
| `occurred_at` | string | ISO-8601, UTC |
| `proof_of_delivery` | object | Only on `DELIVERED` |

## Timestamps
All timestamps returned by the API and sent in webhooks are ISO-8601 in UTC.
