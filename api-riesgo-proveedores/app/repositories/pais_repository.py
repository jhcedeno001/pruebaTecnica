from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.riesgo_proveedor import Pais


"""
Reposiorio encargado de manejar el pais
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class PaisRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def listar_todos(self) -> list[Pais]:
        stmt = select(Pais).order_by(Pais.nombre)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_codigo(self, codigo: str) -> Pais | None:
        codigo = codigo.upper()
        stmt = (
            select(Pais)
            .options(selectinload(Pais.moneda), selectinload(Pais.region))
            .where(or_(Pais.codigo_alfa2 == codigo, Pais.codigo_alfa3 == codigo))
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def upsert(self, pais_existente: Pais | None, campos: dict) -> Pais:
        if pais_existente is None:
            pais = Pais(**campos)
            self._session.add(pais)
        else:
            for campo, valor in campos.items():
                setattr(pais_existente, campo, valor)
            pais = pais_existente

        await self._session.flush()
        return pais
