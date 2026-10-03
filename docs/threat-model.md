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
- Unauthorized read/write: authentication is not implemented. Run only on a trusted local environment; do not expose this service.

## Assumptions and residual risks

The deployment is a local demo using synthetic data. The service has no authentication, authorization, rate limiting, retention policy, encryption configuration, or audit log yet. Metadata is limited by item count but total request body size is not separately capped in this milestone. Production use is out of scope.
