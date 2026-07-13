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
Clase encargada de llamar a clientes externo para obtener informacion adicicional de los paises.
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class ReferenciaGeograficaClient(BaseHttpClient):
    def __init__(self) -> None:
        super().__init__(
            breaker=_breaker,
            limiter=_limiter,
            timeout=settings.geo_reference_api_timeout_seconds,
        )

    async def is_landlocked(self, alpha3_code: str) -> bool | None:
        datos = await self._obtener_dataset()
        if datos is None:
            return None

        mapa = {
            pais["cca3"]: bool(pais.get("landlocked", False))
            for pais in datos
            if isinstance(pais, dict) and "cca3" in pais
        }
        return mapa.get(alpha3_code.upper())

    async def get_catalogo_paises(self) -> list[dict] | None:
        datos = await self._obtener_dataset()
        if datos is None:
            return None

        catalogo = []
        for pais in datos:
            if not isinstance(pais, dict) or "cca2" not in pais or "cca3" not in pais:
                continue
            nombre_es = ((pais.get("translations") or {}).get("spa") or {}).get("common")
            nombre = nombre_es or (pais.get("name") or {}).get("common")
            if not nombre:
                continue
            catalogo.append(
                {"codigo_alfa2": pais["cca2"], "codigo_alfa3": pais["cca3"], "nombre": nombre}
            )
        return catalogo

    async def _obtener_dataset(self) -> list | None:
        async def _pedir() -> list:
            response = await self._client.get(settings.geo_reference_dataset_url)
            response.raise_for_status()
            return response.json()

        try:
            return await self._call(_pedir)
        except CircuitBreakerError:
            logger.warning("Sin respuesta de sistemas externos")
            return None
        except httpx.HTTPError:
            logger.warning("No se pudo obtener información", exc_info=True)
            return None
