from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config.security import verify_token

class JWTMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        # Skip auth for public routes
        if request.url.path in ["/docs", "/openapi.json", "/health", "/auth/login"]:
            return await call_next(request)
        try:
            auth = request.headers.get("Authorization")
            if not auth or not auth.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Missing token")
            token = auth[7:]
            payload = verify_token(token)
            request.state.user_id = payload["sub"]  # Attach user ID
            return await call_next(request)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")