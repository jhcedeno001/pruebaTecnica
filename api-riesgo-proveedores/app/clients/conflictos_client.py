import csv
import io
import logging

import httpx
from aiobreaker import CircuitBreakerError

from app.clients.base import BaseHttpClient, build_resilience
from app.core.config import settings

logger = logging.getLogger(__name__)

_breaker, _limiter = build_resilience(
    settings.http_breaker_fail_max,
    settings.http_breaker_reset_timeout_seconds,
    settings.http_rate_limit_per_second,
)

"""
Clase encargada de llamar a clientes externo de paises en conflicto
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class ConflictosClient(BaseHttpClient):
    def __init__(self) -> None:
        super().__init__(
            breaker=_breaker,
            limiter=_limiter,
            timeout=settings.conflicts_api_timeout_seconds,
        )

    async def get_paises_en_conflicto(self) -> set[str] | None:
        filas = await self._get_filas()
        if not filas:
            return None

        anio_mas_reciente = max(int(fila["year"]) for fila in filas)
        return {
            fila["code"]
            for fila in filas
            if int(fila["year"]) == anio_mas_reciente
            and fila["is_location_of_conflict__conflict_type_all"] == "1"
            and len(fila["code"]) == 3
            and fila["code"].isalpha()
        }

    async def _get_filas(self) -> list[dict] | None:
        async def _pedir() -> str:
            response = await self._client.get(settings.conflicts_dataset_url)
            response.raise_for_status()
            return response.text

        try:
            texto_csv = await self._call(_pedir)
        except CircuitBreakerError:
            logger.warning("No repuesta de información")
            return None
        except httpx.HTTPError:
            logger.warning(
                "No se pudo obtener información", exc_info=True
            )
            return None

        return list(csv.DictReader(io.StringIO(texto_csv)))