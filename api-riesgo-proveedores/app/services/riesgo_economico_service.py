import asyncio
import datetime as dt

from app.clients.tipo_cambio_client import TipoCambioClient
from app.schemas.riesgo_proveedor import IndicadorEconomico, RiesgoEconomico

"""
Variables estaticas para el calculo de riesgos economicos
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
PESO_VARIACION_CAMBIARIA = 1.0
VARIACION_CAMBIARIA_MAX = 20.0
DIAS_HISTORICO_FX = 90
NIVELES_RIESGO_ECONOMICO: list[tuple[float, str, str, int]] = [
    (20, "bajo", "País estable para comerciar.", 0),
    (40, "medio", "Se recomienda monitorear los indicadores económicos.", 1),
    (60, "alto", "Negociar con garantías (anticipos, cartas de crédito).", 2),
    (80, "muy alto", "Exportar solo con fuertes medidas de mitigación.", 3),
    (100, "critico", "Alto riesgo de pérdidas; evaluar otros mercados.", 4),
]


def _clamp(valor: float, minimo: float = 0.0, maximo: float = 100.0) -> float:
    return max(minimo, min(maximo, valor))


def _puntos_lineales(valor: float, minimo: float, maximo: float) -> float:
    if maximo == minimo:
        return 0.0
    proporcion = (valor - minimo) / (maximo - minimo)
    return round(_clamp(proporcion * 100), 2)


def _nivel_por_score(score: float) -> tuple[str, str, int]:
    for limite, nivel, recomendacion, puntos_bucket in NIVELES_RIESGO_ECONOMICO:
        if score <= limite:
            return nivel, recomendacion, puntos_bucket
    _, nivel, recomendacion, puntos_bucket = NIVELES_RIESGO_ECONOMICO[-1]
    return nivel, recomendacion, puntos_bucket

"""
Servicio encargado de gestionar o orquestar el calculo riesgos economicos.
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class RiesgoEconomicoService:
    def __init__(self, tipo_cambio_client: TipoCambioClient) -> None:
        self._tipo_cambio_client = tipo_cambio_client

    """
       Funcion encagada de realizar de calculo riesgos economicos.
       @Author jhcedeno<jose22ced@gmail.com>
       @Version 1.0
    """
    async def calcular_riesgo_economico(self, moneda: str) -> RiesgoEconomico:
        variacion_cambiaria = await self._calcular_variacion_cambiaria(moneda)

        indicadores = [self._indicador_variacion_cambiaria(variacion_cambiaria)]

        score = round(sum(indicador.puntos_ponderados for indicador in indicadores), 2)
        nivel, recomendacion, puntos_bucket = _nivel_por_score(score)

        return RiesgoEconomico(
            score=score,
            nivel=nivel,
            recomendacion=recomendacion,
            puntos_bucket=puntos_bucket,
            indicadores=indicadores,
        )

    """
       Funcion encargada de validar el riesgo por combio de valor de la moneda.
       @Author jhcedeno<jose22ced@gmail.com>
       @Version 1.0
    """
    async def _calcular_variacion_cambiaria(self, moneda: str) -> float | None:
        fecha_historica = dt.date.today() - dt.timedelta(days=DIAS_HISTORICO_FX)
        tasa_actual, tasa_historica = await asyncio.gather(
            self._tipo_cambio_client.get_rate(moneda),
            self._tipo_cambio_client.get_rate(moneda, on_date=fecha_historica),
        )

        if tasa_actual is None or tasa_historica is None or tasa_historica == 0:
            return None

        return ((tasa_actual - tasa_historica) / tasa_historica) * 100

    """
       Metodo estatico para armar objeto del cambio de valor de moneda.
       @Author jhcedeno<jose22ced@gmail.com>
       @Version 1.0
    """
    @staticmethod
    def _indicador_variacion_cambiaria(valor: float | None) -> IndicadorEconomico:
        disponible = valor is not None
        puntos = (
            _puntos_lineales(abs(valor), 0.0, VARIACION_CAMBIARIA_MAX) if disponible else 0.0
        )
        return IndicadorEconomico(
            nombre="variacion_cambiaria",
            valor=valor,
            unidad=f"% ({DIAS_HISTORICO_FX} días)",
            disponible=disponible,
            puntos=puntos,
            peso=PESO_VARIACION_CAMBIARIA,
            puntos_ponderados=round(puntos * PESO_VARIACION_CAMBIARIA, 2),
        )
