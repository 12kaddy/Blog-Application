from fastapi import APIRouter, Depends
from app.api.v1.endpoints import users, posts, comments, auth, admin
from app.core.config.settings import settings
from app.utils.rate_limiter import rate_limiter


def setup_routers() -> APIRouter:
    router = APIRouter(prefix=settings.API_V1_STR)

    # Auth routes with rate limiting
    router.include_router(
        auth.router,
        dependencies=[Depends(rate_limiter)]
    )

    # Other routes
    router.include_router(users.router)
    router.include_router(posts.router)
    router.include_router(comments.router)
    router.include_router(admin.router)

    return router