from sqlalchemy.ext.asyncio import create_async_engine

from .config_env import settings

engine = create_async_engine(url=settings.DATABASE_URL, echo=True)
