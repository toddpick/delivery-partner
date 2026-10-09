# Delivery partner

Parcel collection and last-mile delivery. Clients book parcels through a REST API and receive
status updates by webhook. This repository holds the API contract, the booking and status logic,
and the specifications (spec-driven development) for changes to both.

## Layout

| Path | Contents |
|---|---|
| `specs/` | One folder per feature or integration: requirements, design, tasks, and gate sign-offs. Start with `specs/README.md`. |
| `docs/openapi.yaml` | REST API contract (OpenAPI 3.1) |
| `docs/webhooks.md` | Status webhook contract |
| `docs/data-dictionary.md` | Fields, types, units and enumerations |
| `delivery/` | Models, request validation, delivery windows, webhook payload builder |
| `samples/` | Example requests, responses and webhook bodies |
| `DECISIONS.md` | Decision owners, gate approvers by role, decision log |

## Development

Python 3.12 or newer. The runtime uses the standard library only.

```
python -m pip install -e ".[dev]"
python -m pytest
```

## Working on a change

1. Copy `specs/_templates/` to a new folder and fill in the requirements.
2. Get gates G1 to G4 approved in order (see `specs/README.md`).
3. Implement against the approved design and tasks.

Sample code for integration exercises. All data is fictional.
