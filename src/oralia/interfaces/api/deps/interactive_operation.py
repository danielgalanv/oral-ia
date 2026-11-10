"""Yield before opening a DB transaction; release only after function-scope commit."""

import asyncio

from fastapi import HTTPException, Request


async def interactive_operation(request: Request):
    lock = request.app.state.interactive_operation_lock
    try:
        await asyncio.wait_for(lock.acquire(), timeout=10)
    except TimeoutError:
        raise HTTPException(
            409, "Hay una operación de sesión en curso. Consulta el resultado antes de volver a enviarla."
        ) from None
    try:
        yield
    finally:
        lock.release()
