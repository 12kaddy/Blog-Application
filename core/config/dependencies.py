from typing import Annotated, Optional
from fastapi import Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError
from app.core.database.session import get_db
from app.core.config.security import verify_token
from app.models import User
from app.core.exceptions.http_exceptions import UnauthorizedException, ForbiddenException
# ========================
# Database Dependency
# ========================
DatabaseSession = Annotated[AsyncSession, Depends(get_db)]
# ========================
# Auth Dependencies
# ========================
def get_token_from_header(request: Request) -> str:
    """Extract JWT from Authorization header"""
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise UnauthorizedException("Missing or invalid authorization header")
    return auth[7:]  # Remove 'Bearer ' prefix

async def get_current_user(
    db: DatabaseSession,
    token: str = Depends(get_token_from_header)
) -> User:
    """
    Get authenticated user from JWT
    Args:
        db: Database session
        token: JWT token from header
    Returns:
        User: Authenticated user instance
    Raises:
        UnauthorizedException: If token is invalid or user not found
    """
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")

        if not user_id:
            raise UnauthorizedException("Invalid token payload")

        if not isinstance(user_id, str):
            raise UnauthorizedException("Invalid user ID format")

        user = await db.get(User, int(user_id))

        if not user:
            raise UnauthorizedException("User not found")
        return user

    except JWTError:
        raise UnauthorizedException("Invalid token signature")

    except ValueError:
        raise UnauthorizedException("Invalid token payload")

    except Exception as e:
        raise UnauthorizedException(f"Authentication failed: {str(e)}")

# Typed dependencies for reuse
CurrentUser = Annotated[User, Depends(get_current_user)]

async def get_current_admin(
    user: CurrentUser
) -> User:
    """Verify admin privileges"""
    if user.role != "admin":
        raise ForbiddenException("Admin privileges required")
    return user

AdminUser = Annotated[User, Depends(get_current_admin)]
# ========================
# Optional Auth
# ========================

async def get_optional_user(
    request: Request,
    db: DatabaseSession
) -> Optional[User]:
    """
    Optional authentication dependency
    Returns:
        User: If valid token provided
        None: If no/invalid token
    """
    try:
        token = get_token_from_header(request)
        return await get_current_user(db, token)
    except (UnauthorizedException, HTTPException):
        return None
    except Exception as e:
        import logging
        logging.error(f"Optional auth error: {str(e)}", exc_info=True)
        return None

OptionalUser = Annotated[Optional[User], Depends(get_optional_user)]
# ========================
# Utility Dependencies
# ========================
def get_pagination_params(
    page: int = 1,
    per_page: int = 20,
) -> dict[str, int]:
    """Standardized pagination parameters"""
    return {
        "page": max(1, page),
        "per_page": min(max(1, per_page), 100)
    }
PaginationParams = Annotated[dict[str, int], Depends(get_pagination_params)]