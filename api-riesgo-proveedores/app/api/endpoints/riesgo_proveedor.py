from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.clients.paises_client import PaisesServicioNoDisponibleError, PaisNoEncontradoError
from app.dependencies import get_riesgo_proveedor_service
from app.schemas.riesgo_proveedor import (
    CompareItem,
    HistorialItem,
    PaisResumen,
    RiesgoProveedorResponse,
)
from app.services.riesgo_proveedor_service import RiesgoProveedorService


"""
Apis para las consultas de paises y de sus riesgos
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
router = APIRouter(tags=["supplier-risk"])

"""
Objeto que inicializa los servicios y llamada a las apis externas
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
RiesgoProveedorServiceDep = Annotated[
    RiesgoProveedorService, Depends(get_riesgo_proveedor_service)
]

"""
Controlador que lista el catalogo de paises
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
@router.get("/supplier-risk/countries", response_model=list[PaisResumen])
async def listar_paises_guardados(service: RiesgoProveedorServiceDep) -> list[PaisResumen]:
    return await service.listar_paises()

"""
Controlador que lista el historial de paises buscados anteriormente
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
@router.get("/supplier-risk/history", response_model=list[HistorialItem])
async def obtener_historial_consultas(
        service: RiesgoProveedorServiceDep,
        limite: int = Query(100, ge=1, le=500),
) -> list[HistorialItem]:
    return await service.obtener_historial(limite)

"""
Controlador que compara el riesgo de los paises
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
@router.get("/supplier-risk/compare", response_model=list[CompareItem])
async def comparar_proveedores(
        service: RiesgoProveedorServiceDep,
        countries: str = Query(),
) -> list[CompareItem]:
    codigos = [codigo.strip().upper() for codigo in countries.split(",") if codigo.strip()]
    codigos = list(dict.fromkeys(codigos))

    if len(codigos) < 2:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Se necesitan al menos 2 países para comparar."
        )

    return await service.comparar_paises(codigos)

"""
Controlador que busca el pais y retorna el riesgo
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
@router.get("/supplier-risk/{country}", response_model=RiesgoProveedorResponse)
async def obtener_riesgo_proveedor(
        country: str,
        service: RiesgoProveedorServiceDep,
        refresh: bool = Query(False),
) -> RiesgoProveedorResponse:
    try:
        return await service.evaluar_riesgo_pais(country, refresh=refresh)
    except PaisNoEncontradoError as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"No se encontró el país con código '{country}'",
        ) from exc
    except PaisesServicioNoDisponibleError as exc:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "Se se pudo obtener información. Intentá de nuevo.",
        ) from exc
