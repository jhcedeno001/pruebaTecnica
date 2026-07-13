import httpx
from aiobreaker import CircuitBreakerError

from app.clients.base import BaseHttpClient, build_resilience
from app.core.config import settings

_breaker, _limiter = build_resilience(
    settings.http_breaker_fail_max,
    settings.http_breaker_reset_timeout_seconds,
    settings.http_rate_limit_per_second,
)


class PaisNoEncontradoError(Exception):
    def __init__(self, alpha_code: str) -> None:
        self.alpha_code = alpha_code
        super().__init__(f"País no encontrado para el código '{alpha_code}'")


class PaisesServicioNoDisponibleError(Exception):
    """no respondió a tiempo"""

"""
Clase encargada de llamar a clientes externo para obtener informacion de los paises
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class PaisesClient(BaseHttpClient):
    def __init__(self) -> None:
        super().__init__(
            breaker=_breaker,
            limiter=_limiter,
            base_url=settings.countries_api_base_url,
            timeout=settings.countries_api_timeout_seconds,
        )

    async def get_country(self, alpha_code: str) -> dict:
        async def _pedir() -> httpx.Response:
            response = await self._client.get(f"/alpha/{alpha_code}")
            if response.status_code != 404:
                response.raise_for_status()
            return response

        try:
            response = await self._call(_pedir)
        except CircuitBreakerError as exc:
            raise PaisesServicioNoDisponibleError(
                "Sin respuesta de sistemas externos"
            ) from exc
        except httpx.HTTPError as exc:
            raise PaisesServicioNoDisponibleError(
                f"No respondió correctamente: {exc}"
            ) from exc

        if response.status_code == 404:
            raise PaisNoEncontradoError(alpha_code)
        return response.json()
