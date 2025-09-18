# Import all routers to expose them
from .endpoints import users, posts, comments, auth, admin

__all__ = ["users", "posts", "comments", "auth", "admin"]