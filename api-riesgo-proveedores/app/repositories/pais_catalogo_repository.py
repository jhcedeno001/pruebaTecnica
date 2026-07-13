from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.riesgo_proveedor import PaisCatalogo

"""
Reposiorio encargado de manejar el catalogo de paises
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class PaisCatalogoRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def listar_todos(self) -> list[PaisCatalogo]:
        stmt = select(PaisCatalogo).order_by(PaisCatalogo.nombre)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def existe_alguno(self) -> bool:
        stmt = select(PaisCatalogo.id).limit(1)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def get_by_codigo(self, codigo: str) -> PaisCatalogo | None:
        codigo = codigo.upper()
        stmt = select(PaisCatalogo).where(
            or_(PaisCatalogo.codigo_alfa2 == codigo, PaisCatalogo.codigo_alfa3 == codigo)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def insertar_todos(self, paises: list[dict]) -> None:
        self._session.add_all([PaisCatalogo(**campos) for campos in paises])
        await self._session.flush()
