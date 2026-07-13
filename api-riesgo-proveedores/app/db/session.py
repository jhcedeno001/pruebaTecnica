from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(settings.database_url, echo=settings.debug, future=True)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

"""
Metedo encargado de gestionar la sesion a la base datos.
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
