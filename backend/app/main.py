from fastapi import FastAPI

from app.api.routes.events import router as events_router

app = FastAPI(
    title="SentinelAI API",
    description="Security event ingestion and retrieval API.",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)
app.include_router(events_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
