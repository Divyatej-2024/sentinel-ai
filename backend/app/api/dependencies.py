import hmac
from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(
    provided_key: Annotated[str | None, Security(api_key_header)],
) -> None:
    expected = settings.api_key
    if expected is None:
        return
    if provided_key is None or not hmac.compare_digest(provided_key, expected.get_secret_value()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A valid X-API-Key header is required",
        )


ApiKeyDep = Annotated[None, Depends(require_api_key)]
