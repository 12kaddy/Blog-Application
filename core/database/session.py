from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config.settings import settings
from typing import AsyncGenerator
import contextlib


class DatabaseSessionManager:
    def __init__(self):
        self._engine = None
        self._sessionmaker = None

    def init(self, url: str):
        """Initialize the database connection pool"""
        self._engine = create_async_engine(
            url,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_pre_ping=True,
            echo=settings.DB_ECHO,
            connect_args={
                "command_timeout": 30,
                "server_settings": {
                    "application_name": settings.APP_NAME
                }
            }
        )
        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession
        )

    async def close(self):
        """Close all connections"""
        if self._engine is None:
            return
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncGenerator[AsyncSession, None]:
        """Context manager for individual sessions"""
        if self._sessionmaker is None:
            raise RuntimeError("DatabaseSessionManager is not initialized")
        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Global session manager instance
session_manager = DatabaseSessionManager()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields database sessions
    Automatically handles cleanup on request completion
    """
    async with session_manager.connect() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    """Initialize database connection pool on startup"""
    session_manager.init(str(settings.DATABASE_URL))

async def shutdown_db():
    """Cleanup database connections on shutdown"""
    await session_manager.close()