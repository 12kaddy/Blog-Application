from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED
from app.core.config.settings import settings
from app.core.config.security import verify_token


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if settings.SECURE_HEADERS:
            response.headers.update({
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "DENY",
                "Referrer-Policy": "strict-origin-when-cross-origin"
            })
        return response


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path in ["/docs", "/openapi.json", "/health", "/auth/login"]:
            return await call_next(request)

        try:
            auth = request.headers.get("Authorization")
            if not auth or not auth.startswith("Bearer "):
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Missing token")
            token = auth[7:]
            payload = verify_token(token)
            request.state.user_id = payload["sub"]
            return await call_next(request)
        except Exception as e:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}")