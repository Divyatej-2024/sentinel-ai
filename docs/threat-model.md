# Threat model (Phase 1)

## Assets and boundaries

- Event records, including usernames, hostnames, IP addresses, and metadata.
- Database availability and integrity.
- Trust boundary: untrusted JSON clients -> FastAPI validation -> database network/service.

## Attack surface and mitigations

- Malformed or oversized request fields: Pydantic types, length/port bounds, rejection of unknown properties, and JSON metadata item count bound.
- SQL injection through filters: SQLAlchemy expression parameters; filter names are fixed in code.
- Database exposure: Compose does not publish the PostgreSQL port; credentials are supplied by environment variables.
- Data loss: persistent Docker volume; backups are not yet configured.
- Unauthorized event reads/writes: when `API_KEY` is configured, all event endpoints require a constant-time checked `X-API-Key`. The key is unset for local development; public deployments must set it.

## Assumptions and residual risks

The current frontend is a demo shell, not an analyst console. The service has no user accounts or roles, rate limiting, retention policy, or audit log yet. API keys are shared secrets and do not provide per-user attribution. Metadata is limited by item count but total request body size is not separately capped. Use synthetic data only; production SOC use is out of scope.
