import datetime as dt

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.riesgo_proveedor import Moneda

"""
Reposiorio encargado de manejar la tabla de moneda
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class MonedaRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_or_create(self, siglas: str, tasa_cambio: float | None) -> Moneda | None:
        if not siglas:
            return None

        stmt = select(Moneda).where(Moneda.siglas == siglas.upper())
        result = await self._session.execute(stmt)
        moneda = result.scalar_one_or_none()

        if moneda is None:
            moneda = Moneda(siglas=siglas.upper(), nombre=siglas.upper(), tasa_cambio=tasa_cambio)
            self._session.add(moneda)
        elif tasa_cambio is not None:
            moneda.tasa_cambio = tasa_cambio
            moneda.actualizado_en = dt.datetime.utcnow()

        await self._session.flush()
        return moneda
