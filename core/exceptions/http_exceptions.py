from fastapi import HTTPException, status

class AppException(HTTPException):
    """Base exception with customizable status code"""
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)
        self.type = self.__class__.__name__

class NotFoundException(AppException):
    """404 Not Found"""
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            detail=f"{resource} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

class ForbiddenException(AppException):
    """403 Forbidden"""
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_403_FORBIDDEN
        )

class UnauthorizedException(AppException):
    """401 Unauthorized"""
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_401_UNAUTHORIZED
        )

class ConflictException(AppException):
    """409 Conflict"""
    def __init__(self, detail: str = "Conflict"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_409_CONFLICT
        )

class RateLimitException(AppException):
    """429 Too Many Requests"""
    def __init__(self, detail: str = "Too many requests"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )