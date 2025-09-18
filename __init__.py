# Expose main app components for easy importing
from app.main import app
from app.core.config.settings import settings
from app.models import User

__all__ = ["app", "settings"]