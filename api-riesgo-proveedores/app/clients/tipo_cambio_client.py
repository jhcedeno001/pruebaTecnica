import datetime as dt
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
Clase encargada de llamar a clientes externo para obtener el valor de cambio de su moneda.
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class TipoCambioClient(BaseHttpClient):
    def __init__(self) -> None:
        super().__init__(
            breaker=_breaker,
            limiter=_limiter,
            timeout=settings.exchange_rate_api_timeout_seconds,
            follow_redirects=True,
        )

    async def get_rate(self, target_currency: str, on_date: dt.date | None = None) -> float | None:
        if target_currency == "USD":
            return 1.0

        version = "latest" if on_date is None else on_date.isoformat()

        data = await self._fetch_data(settings.exchange_rate_primary_url.format(version=version))
        if data is None:
            data = await self._fetch_data(
                settings.exchange_rate_fallback_url.format(version=version)
            )

        if data is None:
            return None

        rate = data.get("usd", {}).get(target_currency.lower())
        return float(rate) if rate is not None else None

    async def _fetch_data(self, url: str) -> dict | None:
        async def _pedir() -> dict:
            response = await self._client.get(url)
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
