from app.clients.conflictos_client import ConflictosClient
from app.clients.referencia_geografica_client import ReferenciaGeograficaClient
from app.schemas.riesgo_proveedor import FactorRiesgo, PaisInfo, RiesgoGeopolitico

"""
Variables estaticas para el calculo de riesgos geopoliticos
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
UMBRAL_POCAS_FRONTERAS = 1

PUNTOS_LANDLOCKED = 2
PUNTOS_POCAS_FRONTERAS = 1
PUNTOS_CONFLICTO_PROPIO = 1
PUNTOS_VECINO_CONFLICTO = 1
SCORE_MAXIMO = (
    PUNTOS_LANDLOCKED + PUNTOS_POCAS_FRONTERAS + PUNTOS_CONFLICTO_PROPIO + PUNTOS_VECINO_CONFLICTO
)

def _nivel_riesgo(score_total: int) -> str:
    if score_total == 0:
        return "bajo"
    if score_total == 1:
        return "medio"
    if score_total == 2:
        return "alto"
    if score_total <= 4:
        return "muy alto"
    return "critico"

"""
Servicio encargado de gestionar o orquestar el calculo riesgos geopoliticos.
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class RiesgoGeopoliticoService:
    def __init__(
        self,
        referencia_geografica_client: ReferenciaGeograficaClient,
        conflictos_client: ConflictosClient,
    ) -> None:
        self._referencia_geografica_client = referencia_geografica_client
        self._conflictos_client = conflictos_client

    """
    Funcion encargada de realizar calculos de riesgos geopoliticos con información de la api externa
    @Author jhcedeno<jose22ced@gmail.com>
    @Version 1.0
    """
    async def calcular_riesgo_geopolitico(self, pais: PaisInfo) -> RiesgoGeopolitico:
        paises_en_conflicto = await self._conflictos_client.get_paises_en_conflicto()

        desglose = [
            await self._factor_landlocked(pais),
            self._factor_pocas_fronteras(pais),
            self._factor_conflicto_propio(pais, paises_en_conflicto),
            self._factor_vecino_en_conflicto(pais, paises_en_conflicto),
        ]
        score_total = sum(factor.puntos for factor in desglose)
        return RiesgoGeopolitico(
            score_total=score_total,
            score_maximo=SCORE_MAXIMO,
            nivel=_nivel_riesgo(score_total),
            desglose=desglose,
        )

    """
    Funcion encargada de validar que el pais tenga salida al mar
    @Author jhcedeno<jose22ced@gmail.com>
    @Version 1.0
    """
    async def _factor_landlocked(self, pais: PaisInfo) -> FactorRiesgo:
        landlocked = await self._referencia_geografica_client.is_landlocked(pais.alpha3)
        aplica = bool(landlocked)
        return FactorRiesgo(
            factor="sin_salida_al_mar",
            descripcion="País sin salida al mar",
            aplica=aplica,
            puntos=PUNTOS_LANDLOCKED if aplica else 0,
            detalle={"alpha3": pais.alpha3, "dato_disponible": landlocked is not None},
        )

    """
    Funcion encargada de validar si el pais tiene fronteras
    @Author jhcedeno<jose22ced@gmail.com>
    @Version 1.0
    """
    @staticmethod
    def _factor_pocas_fronteras(pais: PaisInfo) -> FactorRiesgo:
        cantidad = len(pais.fronteras)
        aplica = cantidad <= UMBRAL_POCAS_FRONTERAS
        return FactorRiesgo(
            factor="pocas_fronteras_terrestres",
            descripcion="Pocas fronteras terrestres: menos rutas alternativas de tránsito",
            aplica=aplica,
            puntos=PUNTOS_POCAS_FRONTERAS if aplica else 0,
            detalle={"cantidad_fronteras": cantidad, "umbral": UMBRAL_POCAS_FRONTERAS},
        )

    """
    Funcion encargada de validar si el pais se encuntra en conflicto
    @Author jhcedeno<jose22ced@gmail.com>
    @Version 1.0
    """
    @staticmethod
    def _factor_conflicto_propio(
        pais: PaisInfo, paises_en_conflicto: set[str] | None
    ) -> FactorRiesgo:
        dato_disponible = paises_en_conflicto is not None
        aplica = dato_disponible and pais.alpha3 in paises_en_conflicto
        return FactorRiesgo(
            factor="conflicto_armado_propio",
            descripcion="El país registra conflicto armado activo",
            aplica=aplica,
            puntos=PUNTOS_CONFLICTO_PROPIO if aplica else 0,
            detalle={"alpha3": pais.alpha3, "dato_disponible": dato_disponible},
        )

    """
    Funcion encargada de validar el prooveror tiene algun pais vecino en conflicto
    @Author jhcedeno<jose22ced@gmail.com>
    @Version 1.0
    """
    @staticmethod
    def _factor_vecino_en_conflicto(
        pais: PaisInfo, paises_en_conflicto: set[str] | None
    ) -> FactorRiesgo:
        dato_disponible = paises_en_conflicto is not None
        vecinos_en_conflicto = (
            sorted(set(pais.fronteras) & paises_en_conflicto) if dato_disponible else []
        )
        aplica = bool(vecinos_en_conflicto)
        return FactorRiesgo(
            factor="vecino_en_conflicto",
            descripcion="Limita con al menos un país con conflicto armado activo",
            aplica=aplica,
            puntos=PUNTOS_VECINO_CONFLICTO if aplica else 0,
            detalle={"vecinos_en_conflicto": vecinos_en_conflicto, "dato_disponible": dato_disponible},
        )
