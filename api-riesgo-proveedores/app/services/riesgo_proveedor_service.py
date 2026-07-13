import datetime as dt

from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.paises_client import (
    PaisesClient,
    PaisesServicioNoDisponibleError,
    PaisNoEncontradoError,
)
from app.clients.tipo_cambio_client import TipoCambioClient
from app.models.riesgo_proveedor import Pais, PaisDetalle
from app.repositories.moneda_repository import MonedaRepository
from app.repositories.pais_catalogo_repository import PaisCatalogoRepository
from app.repositories.pais_detalle_repository import PaisDetalleRepository
from app.repositories.pais_repository import PaisRepository
from app.repositories.region_repository import RegionRepository
from app.schemas.riesgo_proveedor import (
    CompareItem,
    HistorialItem,
    PaisInfo,
    PaisResumen,
    RiesgoProveedorResponse,
)
from app.services.riesgo_economico_service import RiesgoEconomicoService
from app.services.riesgo_geopolitico_service import RiesgoGeopoliticoService


NIVELES_COMBINADOS: list[tuple[int, str]] = [
    (1, "bajo"),
    (3, "medio"),
    (5, "alto"),
    (7, "muy alto"),
    (9, "critico"),
]

"""
Servicio encargado de gestionar o orquestar funiones de los paises
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class RiesgoProveedorService:
    def __init__(
        self,
        paises_client: PaisesClient,
        tipo_cambio_client: TipoCambioClient,
        riesgo_economico_service: RiesgoEconomicoService,
        riesgo_geopolitico_service: RiesgoGeopoliticoService,
        pais_repository: PaisRepository,
        pais_catalogo_repository: PaisCatalogoRepository,
        moneda_repository: MonedaRepository,
        region_repository: RegionRepository,
        pais_detalle_repository: PaisDetalleRepository,
        session: AsyncSession,
    ) -> None:
        self._paises_client = paises_client
        self._tipo_cambio_client = tipo_cambio_client
        self._riesgo_economico_service = riesgo_economico_service
        self._riesgo_geopolitico_service = riesgo_geopolitico_service
        self._pais_repository = pais_repository
        self._pais_catalogo_repository = pais_catalogo_repository
        self._moneda_repository = moneda_repository
        self._region_repository = region_repository
        self._pais_detalle_repository = pais_detalle_repository
        self._session = session

    """
    Funcion encargada de construir y guardar el objetos de los riesgos geopolitos y economicos
    @Author jhcedeno<jose22ced@gmail.com>
    @Version 1.0
    """
    async def evaluar_riesgo_pais(
        self, alpha_code: str, refresh: bool = False
    ) -> RiesgoProveedorResponse:
        pais_bd = await self._pais_repository.get_by_codigo(alpha_code)

        if pais_bd is None or refresh:
            data = await self._paises_client.get_country(alpha_code)
            pais_bd = await self._guardar_pais_desde_payload(data, pais_bd)

        pais = self._pais_info_desde_bd(pais_bd)

        riesgo_geopolitico = await self._riesgo_geopolitico_service.calcular_riesgo_geopolitico(
            pais
        )
        riesgo_economico = await self._riesgo_economico_service.calcular_riesgo_economico(
            pais.moneda
        )

        score_total = riesgo_geopolitico.score_total + riesgo_economico.puntos_bucket
        nivel_combinado = self._nivel_combinado(score_total)

        await self._pais_detalle_repository.registrar_consulta(
            PaisDetalle(
                pais_id=pais_bd.id,
                score_geopolitico=riesgo_geopolitico.score_total,
                score_economico=riesgo_economico.score,
                variacion_cambiaria=riesgo_economico.indicadores[0].valor,
                score_total=score_total,
                nivel_combinado=nivel_combinado,
                consultado_en=dt.datetime.utcnow(),
            )
        )
        await self._session.commit()

        return RiesgoProveedorResponse(
            pais=pais,
            riesgo_geopolitico=riesgo_geopolitico,
            riesgo_economico=riesgo_economico,
            score_total=score_total,
            nivel_combinado=nivel_combinado,
        )

    """
    Funcion encargada de construir y obtener información guardada en base datos
    @Author jhcedeno<jose22ced@gmail.com>
    @Version 1.0
    """
    async def obtener_historial(self, limite: int = 100) -> list[HistorialItem]:
        detalles = await self._pais_detalle_repository.listar_historial(limite)
        return [
            HistorialItem(
                pais_alpha2=detalle.pais.codigo_alfa2,
                pais_alpha3=detalle.pais.codigo_alfa3,
                pais_nombre=detalle.pais.nombre,
                pais_bandera_url=detalle.pais.bandera_url,
                score_total=detalle.score_total,
                nivel_combinado=detalle.nivel_combinado,
                consultado_en=detalle.consultado_en,
            )
            for detalle in detalles
        ]

    """
    Funcion encargada de construir un VS del riesgo de una lista de paises.
    @Author jhcedeno<jose22ced@gmail.com>
    @Version 1.0
    """
    async def comparar_paises(self, alpha_codes: list[str]) -> list[CompareItem]:
        resultados: list[CompareItem] = []
        for codigo in alpha_codes:
            try:
                riesgo = await self.evaluar_riesgo_pais(codigo)
                resultados.append(
                    CompareItem(
                        codigo_solicitado=codigo,
                        ok=True,
                        pais_nombre=riesgo.pais.nombre,
                        pais_alpha2=riesgo.pais.alpha2,
                        score_geopolitico=riesgo.riesgo_geopolitico.score_total,
                        score_economico=riesgo.riesgo_economico.score,
                        score_total=riesgo.score_total,
                        nivel_combinado=riesgo.nivel_combinado,
                    )
                )
            except PaisNoEncontradoError:
                resultados.append(
                    CompareItem(codigo_solicitado=codigo, ok=False, error="País no encontrado")
                )
            except PaisesServicioNoDisponibleError:
                resultados.append(
                    CompareItem(
                        codigo_solicitado=codigo,
                        ok=False,
                        error="countries.dev no respondió",
                    )
                )
        return resultados

    """
    Funcion encargada de construiar el objeto con los paises del catalogo  
    @Author jhcedeno<jose22ced@gmail.com>
    @Version 1.0
    """
    async def listar_paises(self) -> list[PaisResumen]:
        paises = await self._pais_catalogo_repository.listar_todos()
        return [
            PaisResumen(nombre=pais.nombre, codigo_alfa2=pais.codigo_alfa2) for pais in paises
        ]

    """
    Funcion encargada de construir el objeto, guardar la información nueva y evaluar la que la info no exista en la base datos.
    @Author jhcedeno<jose22ced@gmail.com>
    @Version 1.0
    """
    async def _guardar_pais_desde_payload(self, data: dict, pais_existente: Pais | None) -> Pais:
        moneda_siglas = (data.get("currencies") or [{}])[0].get("code", "")
        tasa_actual = (
            await self._tipo_cambio_client.get_rate(moneda_siglas) if moneda_siglas else None
        )
        moneda = await self._moneda_repository.get_or_create(moneda_siglas, tasa_actual)
        region = await self._region_repository.get_or_create(data.get("region") or "")
        catalogo_pais = await self._pais_catalogo_repository.get_by_codigo(data["alpha2Code"])
        nombre = catalogo_pais.nombre if catalogo_pais else data["name"]

        campos = {
            "codigo_alfa2": data["alpha2Code"],
            "codigo_alfa3": data["alpha3Code"],
            "nombre": nombre,
            "subregion": data.get("subregion") or None,
            "bandera_url": (data.get("flags") or {}).get("png"),
            "capital": data.get("capital"),
            "poblacion": data.get("population"),
            "area": data.get("area"),
            "poblacion_densidad": data.get("populationDensity"),
            "fronteras": data.get("borders") or [],
        }
        pais_bd = await self._pais_repository.upsert(pais_existente, campos)
        pais_bd.moneda = moneda
        pais_bd.region = region
        await self._session.flush()
        return pais_bd

    """
      Metodo estatico para armar un objeto PaisInfo
      @Author jhcedeno<jose22ced@gmail.com>
      @Version 1.0
    """
    @staticmethod
    def _pais_info_desde_bd(pais_bd: Pais) -> PaisInfo:
        return PaisInfo(
            nombre=pais_bd.nombre,
            alpha2=pais_bd.codigo_alfa2,
            alpha3=pais_bd.codigo_alfa3,
            region=pais_bd.region.nombre if pais_bd.region else "",
            subregion=pais_bd.subregion or "",
            poblacion=pais_bd.poblacion or 0,
            area=pais_bd.area,
            poblacion_densidad=pais_bd.poblacion_densidad,
            fronteras=pais_bd.fronteras or [],
            moneda=pais_bd.moneda.siglas if pais_bd.moneda else "",
        )

    """
        Metodo estatico para setar un nivel de riesgo.
        @Author jhcedeno<jose22ced@gmail.com>
        @Version 1.0
    """
    @staticmethod
    def _nivel_combinado(score_total: int) -> str:
        for limite, nivel in NIVELES_COMBINADOS:
            if score_total <= limite:
                return nivel
        return NIVELES_COMBINADOS[-1][1]
