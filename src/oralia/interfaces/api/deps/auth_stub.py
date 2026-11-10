"""Historical dependency name retained for real Feature 005 teacher authorization."""

from __future__ import annotations

from fastapi import HTTPException, Request


async def tecnica_access_control(request: Request) -> None:
    """Feature 005 replaces the historical extension point with real authorization."""
    grant = getattr(request.state, "access_grant", None)
    if grant is None or grant.role != "teacher":
        raise HTTPException(403, "teacher access required")
