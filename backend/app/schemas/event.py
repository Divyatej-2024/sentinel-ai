from datetime import datetime, timezone
from ipaddress import IPv4Address, IPv6Address
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

NonEmpty = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
IPAddress = IPv4Address | IPv6Address


class SecurityEventCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timestamp: datetime
    event_type: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=64)]
    source: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=128)]
    source_ip: IPAddress | None = None
    destination_ip: IPAddress | None = None
    source_port: int | None = Field(default=None, ge=1, le=65535)
    destination_port: int | None = Field(default=None, ge=1, le=65535)
    protocol: Annotated[str, StringConstraints(strip_whitespace=True, max_length=32)] | None = None
    username: NonEmpty | None = None
    hostname: NonEmpty | None = None
    process_name: NonEmpty | None = None
    action: Annotated[str, StringConstraints(strip_whitespace=True, max_length=128)] | None = None
    status: Annotated[str, StringConstraints(strip_whitespace=True, max_length=64)] | None = None
    severity: Literal["low", "medium", "high", "critical"] | None = None
    message: str | None = Field(default=None, max_length=10000)
    metadata: dict[str, Any] = Field(default_factory=dict, max_length=100)

    @field_validator("timestamp")
    @classmethod
    def normalize_timestamp(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("timestamp must include a timezone")
        return value.astimezone(timezone.utc)


class SecurityEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    event_id: UUID
    timestamp: datetime
    event_type: str
    source: str
    source_ip: str | None
    destination_ip: str | None
    source_port: int | None
    destination_port: int | None
    protocol: str | None
    username: str | None
    hostname: str | None
    process_name: str | None
    action: str | None
    status: str | None
    severity: str | None
    message: str | None
    metadata: dict[str, Any] = Field(validation_alias="event_metadata")
    created_at: datetime
