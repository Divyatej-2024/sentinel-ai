# Architecture

Phase 1 is a small monolith: FastAPI owns validation and HTTP concerns; Pydantic schemas define the external contract; SQLAlchemy models and repositories through sessions own persistence; PostgreSQL is the deployment database. Alembic tracks schema changes. The Next.js app is a shell for future analyst workflows.

The normalized event has common nullable fields plus a bounded JSON metadata object for source-specific attributes. No detection, correlation, AI, or response action is implemented in this phase. See the repository README for local startup.
