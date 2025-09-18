from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from app.core.config.settings import settings
import asyncio

_rate_limit_storage = {}
_lock = asyncio.Lock()


async def rate_limiter(request: Request):
    if not settings.RATE_LIMITING_ENABLED:
        return

    client_ip = request.client.host if request.client else "127.0.0.1"
    path = request.url.path
    key = f"{client_ip}:{path}"

    async with _lock:
        now = datetime.now()
        last_time, count = _rate_limit_storage.get(key, (now, 0))

        if now - last_time > timedelta(minutes=1):
            _rate_limit_storage[key] = (now, 1)
        elif count >= settings.RATE_LIMIT:
            raise HTTPException(
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests"
            )
        else:
            _rate_limit_storage[key] = (last_time, count + 1)