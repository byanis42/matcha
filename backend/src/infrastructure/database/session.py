from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from ...config.settings import get_settings

settings = get_settings()

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

# Create async session factory
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Base class for all models
class Base(DeclarativeBase):
    pass


# Database initialization
async def init_db():
    """Initialize database connection"""
    async with engine.begin():
        # Import all models here to ensure they are registered
        # In production, use Alembic migrations instead
        # await conn.run_sync(Base.metadata.create_all)
        pass


# Dependency to get database session
async def get_db() -> AsyncSession:
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
