from collections.abc import Awaitable, Callable
from datetime import timedelta
from types import TracebackType
from typing import Any, Self, TypeVar

import httpx
from aiobreaker import CircuitBreaker
from aiolimiter import AsyncLimiter

T = TypeVar("T")


def build_resilience(
        fail_max: int, reset_timeout_seconds: float, rate_limit_per_second: float
) -> tuple[CircuitBreaker, AsyncLimiter]:
    breaker = CircuitBreaker(
        fail_max=fail_max, timeout_duration=timedelta(seconds=reset_timeout_seconds)
    )
    limiter = AsyncLimiter(rate_limit_per_second, 1)
    return breaker, limiter

"""
Servicio encargado de llamar a clientes externos
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class BaseHttpClient:
    def __init__(
            self,
            *,
            breaker: CircuitBreaker,
            limiter: AsyncLimiter,
            **httpx_kwargs: Any,
    ) -> None:
        self._client = httpx.AsyncClient(**httpx_kwargs)
        self._breaker = breaker
        self._limiter = limiter

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc: BaseException | None,
            tb: TracebackType | None,
    ) -> None:
        await self._client.aclose()

    async def _call(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        async with self._limiter:
            return await self._breaker.call_async(func, *args, **kwargs)
