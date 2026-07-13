from sqlalchemy.ext.asyncio import AsyncEngine

from app.db.base import Base


"""
Metodo encargado de crear las tablas al inicializar el sistema.
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class SchemaInitializer:
    def __init__(self, engine: AsyncEngine) -> None:
        self._engine = engine

    async def crear_tablas(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
