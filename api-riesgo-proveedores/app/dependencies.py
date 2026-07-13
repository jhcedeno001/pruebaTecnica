from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.conflictos_client import ConflictosClient
from app.clients.paises_client import PaisesClient
from app.clients.referencia_geografica_client import ReferenciaGeograficaClient
from app.clients.tipo_cambio_client import TipoCambioClient
from app.db.session import get_db
from app.repositories.moneda_repository import MonedaRepository
from app.repositories.pais_catalogo_repository import PaisCatalogoRepository
from app.repositories.pais_detalle_repository import PaisDetalleRepository
from app.repositories.pais_repository import PaisRepository
from app.repositories.region_repository import RegionRepository
from app.services.riesgo_economico_service import RiesgoEconomicoService
from app.services.riesgo_geopolitico_service import RiesgoGeopoliticoService
from app.services.riesgo_proveedor_service import RiesgoProveedorService

"""
Dependecias de las funiones que se van a usar
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""

async def get_paises_client() -> AsyncGenerator[PaisesClient, None]:
    async with PaisesClient() as client:
        yield client


async def get_tipo_cambio_client() -> AsyncGenerator[TipoCambioClient, None]:
    async with TipoCambioClient() as client:
        yield client


async def get_referencia_geografica_client() -> AsyncGenerator[
    ReferenciaGeograficaClient, None
]:
    async with ReferenciaGeograficaClient() as client:
        yield client


async def get_conflictos_client() -> AsyncGenerator[ConflictosClient, None]:
    async with ConflictosClient() as client:
        yield client


def get_riesgo_economico_service(
        tipo_cambio_client: Annotated[TipoCambioClient, Depends(get_tipo_cambio_client)],
) -> RiesgoEconomicoService:
    return RiesgoEconomicoService(tipo_cambio_client)


def get_riesgo_geopolitico_service(
        referencia_geografica_client: Annotated[
            ReferenciaGeograficaClient, Depends(get_referencia_geografica_client)
        ],
        conflictos_client: Annotated[ConflictosClient, Depends(get_conflictos_client)],
) -> RiesgoGeopoliticoService:
    return RiesgoGeopoliticoService(referencia_geografica_client, conflictos_client)


def get_pais_repository(
        session: Annotated[AsyncSession, Depends(get_db)],
) -> PaisRepository:
    return PaisRepository(session)


def get_pais_catalogo_repository(
        session: Annotated[AsyncSession, Depends(get_db)],
) -> PaisCatalogoRepository:
    return PaisCatalogoRepository(session)


def get_moneda_repository(
        session: Annotated[AsyncSession, Depends(get_db)],
) -> MonedaRepository:
    return MonedaRepository(session)


def get_region_repository(
        session: Annotated[AsyncSession, Depends(get_db)],
) -> RegionRepository:
    return RegionRepository(session)


def get_pais_detalle_repository(
        session: Annotated[AsyncSession, Depends(get_db)],
) -> PaisDetalleRepository:
    return PaisDetalleRepository(session)


def get_riesgo_proveedor_service(
        paises_client: Annotated[PaisesClient, Depends(get_paises_client)],
        tipo_cambio_client: Annotated[TipoCambioClient, Depends(get_tipo_cambio_client)],
        riesgo_economico_service: Annotated[
            RiesgoEconomicoService, Depends(get_riesgo_economico_service)
        ],
        riesgo_geopolitico_service: Annotated[
            RiesgoGeopoliticoService, Depends(get_riesgo_geopolitico_service)
        ],
        pais_repository: Annotated[PaisRepository, Depends(get_pais_repository)],
        pais_catalogo_repository: Annotated[
            PaisCatalogoRepository, Depends(get_pais_catalogo_repository)
        ],
        moneda_repository: Annotated[MonedaRepository, Depends(get_moneda_repository)],
        region_repository: Annotated[RegionRepository, Depends(get_region_repository)],
        pais_detalle_repository: Annotated[
            PaisDetalleRepository, Depends(get_pais_detalle_repository)
        ],
        session: Annotated[AsyncSession, Depends(get_db)],
) -> RiesgoProveedorService:
    return RiesgoProveedorService(
        paises_client,
        tipo_cambio_client,
        riesgo_economico_service,
        riesgo_geopolitico_service,
        pais_repository,
        pais_catalogo_repository,
        moneda_repository,
        region_repository,
        pais_detalle_repository,
        session,
    )
