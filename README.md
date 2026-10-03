# SentinelAI

SentinelAI is an early-stage, locally runnable security operations platform. This first milestone provides a typed event ingestion API and persistent event store; deterministic detections and analyst workflows are planned for later phases.

## Architecture

```text
JSON source -> FastAPI validation -> SQLAlchemy -> PostgreSQL
                         |              |
                         +-- OpenAPI    +-- Alembic migrations
```

The backend is deliberately synchronous and modular for this small first release. The web app is a minimal Next.js shell. No AI or automatic response actions are implemented.

## Features

- Normalized security events with source-specific JSON metadata
- Event creation, retrieval, pagination, and field filters
- OpenAPI docs at `/api/docs` and `/api/redoc`
- PostgreSQL in Docker Compose; SQLite is supported for lightweight local tests

## Requirements

- Docker Desktop with Compose, or Python 3.12+ and PostgreSQL 16+
- Node.js 20+ only when running the frontend outside Docker

## Run with Docker

Copy `.env.example` to `.env`, then run:

```sh
docker compose up --build
```

The API is at `http://localhost:8000`, docs at `http://localhost:8000/api/docs`, and the frontend at `http://localhost:3000`. Compose waits for PostgreSQL health and applies Alembic migrations before starting the API. The example database password is for local development only; set your own values for any shared environment.

## Public demo deployment

For a public Render deployment, follow [docs/deploy-render.md](docs/deploy-render.md). The free Blueprint exposes the app publicly but the database expires after 30 days. Configure a paid database plan for persistent operation.

## Run the backend locally

From `backend/`, create a virtual environment, install the project, and configure `DATABASE_URL` (for example `postgresql+psycopg://sentinel:sentinel@localhost:5432/sentinel`). Then:

```sh
python -m pip install -e '.[dev]'
alembic upgrade head
uvicorn app.main:app --reload
```

Run tests from `backend/` with `pytest`.

## API example

```sh
curl -X POST http://localhost:8000/api/v1/events \
  -H 'Content-Type: application/json' \
  -d '{"timestamp":"2026-10-03T12:00:00Z","event_type":"authentication","source":"windows","source_ip":"192.168.1.50","username":"administrator","hostname":"WORKSTATION-01","action":"login","status":"failed"}'
```

List events with `GET /api/v1/events?limit=50&offset=0&severity=high`. Supported filters include `start_time`, `end_time`, `event_type`, `source`, `severity`, `hostname`, `username`, `source_ip`, and `status`.

## Security and limitations

For public deployment, configure `API_KEY`; all event endpoints then require it in the `X-API-Key` request header. Keep the key private. The app has no user accounts or roles, audit log, or rate limiting, and is still an early demo. Use synthetic data only and do not send sensitive production telemetry. Input is schema validated, IP fields are parsed, and query filters use parameterized SQLAlchemy expressions. Secrets are supplied through environment variables rather than committed configuration.

See [docs/architecture.md](docs/architecture.md), [docs/detection-engine.md](docs/detection-engine.md), [docs/risk-scoring.md](docs/risk-scoring.md), [docs/api.md](docs/api.md), and [docs/threat-model.md](docs/threat-model.md) for design notes. Future work includes alerts, deterministic detection, correlation, incidents, audit logs, authentication, and AI-assisted investigation behind analyst approval.
