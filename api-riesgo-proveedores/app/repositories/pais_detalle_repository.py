from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.riesgo_proveedor import PaisDetalle

"""
Reposiorio encargado de manejar el detalle de paises
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class PaisDetalleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def registrar_consulta(self, detalle: PaisDetalle) -> PaisDetalle:
        self._session.add(detalle)
        await self._session.flush()
        return detalle

    async def listar_historial(self, limite: int = 100) -> list[PaisDetalle]:
        stmt = (
            select(PaisDetalle)
            .options(selectinload(PaisDetalle.pais))
            .order_by(PaisDetalle.consultado_en.desc())
            .limit(limite)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
