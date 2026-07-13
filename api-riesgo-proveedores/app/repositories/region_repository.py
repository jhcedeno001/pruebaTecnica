from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.riesgo_proveedor import Region

"""
Reposiorio encargado de manejar la region
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class RegionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_or_create(self, nombre: str) -> Region | None:
        if not nombre:
            return None

        stmt = select(Region).where(Region.nombre == nombre)
        result = await self._session.execute(stmt)
        region = result.scalar_one_or_none()

        if region is None:
            region = Region(nombre=nombre, tensiones_diplomaticas=False)
            self._session.add(region)

        await self._session.flush()
        return region
