from fastapi import HTTPException, status
from pydantic import ValidationError
from typing import List, Dict, Any

def format_validation_error(err: ValidationError) -> List[Dict[str, Any]]:
    """Convert Pydantic errors to frontend-friendly format"""
    return [
        {
            "field": "->".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        }
        for error in err.errors()
    ]

class ValidationException(HTTPException):
    """Custom 422 validation error with structured response"""
    def __init__(self, error: ValidationError):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "code": "validation_error",
                "errors": format_validation_error(error)
            }
        )