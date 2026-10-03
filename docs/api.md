# API

The FastAPI OpenAPI specification is served at `/api/openapi.json`; interactive docs are at `/api/docs` and `/api/redoc`.

- `POST /api/v1/events`: validate and store one normalized event.
- `GET /api/v1/events`: list newest events with `limit` (1–200) and `offset` pagination and optional filters `start_time`, `end_time`, `event_type`, `source`, `severity`, `hostname`, `username`, `source_ip`, and `status`.
- `GET /api/v1/events/{event_id}`: retrieve an event by UUID.
- `GET /health`: liveness endpoint.

Time values must include a timezone. Event timestamps are normalized to UTC. Unknown input properties are rejected.
