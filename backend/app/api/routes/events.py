from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic.networks import IPvAnyAddress
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.models import SecurityEvent
from app.schemas.event import SecurityEventCreate, SecurityEventRead

router = APIRouter(prefix="/events", tags=["events"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("", response_model=SecurityEventRead, status_code=status.HTTP_201_CREATED)
def create_event(payload: SecurityEventCreate, session: SessionDep) -> SecurityEvent:
    values = payload.model_dump(exclude={"metadata"})
    values["source_ip"] = str(payload.source_ip) if payload.source_ip else None
    values["destination_ip"] = str(payload.destination_ip) if payload.destination_ip else None
    values["event_metadata"] = payload.metadata
    event = SecurityEvent(**values)
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@router.get("", response_model=list[SecurityEventRead])
def list_events(
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    event_type: str | None = Query(default=None, max_length=64),
    source: str | None = Query(default=None, max_length=128),
    severity: str | None = Query(default=None, pattern="^(low|medium|high|critical)$"),
    hostname: str | None = Query(default=None, max_length=255),
    username: str | None = Query(default=None, max_length=255),
    source_ip: IPvAnyAddress | None = None,
    status: str | None = Query(default=None, max_length=64),
) -> list[SecurityEvent]:
    if start_time and start_time.tzinfo is None:
        raise HTTPException(status_code=422, detail="start_time must include a timezone")
    if end_time and end_time.tzinfo is None:
        raise HTTPException(status_code=422, detail="end_time must include a timezone")
    if start_time and end_time and start_time > end_time:
        raise HTTPException(status_code=422, detail="start_time must not be after end_time")

    statement = select(SecurityEvent)
    filters = {
        "event_type": event_type,
        "source": source,
        "severity": severity,
        "hostname": hostname,
        "username": username,
        "source_ip": source_ip,
        "status": status,
    }
    for field, value in filters.items():
        if value is not None:
            if field == "source_ip":
                value = str(value)
            statement = statement.where(getattr(SecurityEvent, field) == value)
    if start_time:
        statement = statement.where(SecurityEvent.timestamp >= start_time)
    if end_time:
        statement = statement.where(SecurityEvent.timestamp <= end_time)
    statement = (
        statement.order_by(SecurityEvent.timestamp.desc(), SecurityEvent.event_id.desc())
        .offset(offset)
        .limit(limit)
    )
    return list(session.scalars(statement).all())


@router.get("/{event_id}", response_model=SecurityEventRead)
def get_event(event_id: UUID, session: SessionDep) -> SecurityEvent:
    event = session.get(SecurityEvent, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
