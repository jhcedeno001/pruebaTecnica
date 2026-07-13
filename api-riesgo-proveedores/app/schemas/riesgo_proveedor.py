import datetime as dt

from pydantic import BaseModel


"""
DTOS de PaisInfo
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class PaisInfo(BaseModel):
    nombre: str
    alpha2: str
    alpha3: str
    region: str
    subregion: str
    poblacion: int
    area: float | None
    poblacion_densidad: float | None
    fronteras: list[str]
    moneda: str

"""
DTOS de FactorRiesgo
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class FactorRiesgo(BaseModel):
    factor: str
    descripcion: str
    aplica: bool
    puntos: int
    detalle: dict

"""
DTOS de RiesgoGeopolitico
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class RiesgoGeopolitico(BaseModel):
    score_total: int
    score_maximo: int
    nivel: str
    desglose: list[FactorRiesgo]

"""
DTOS de IndicadorEconomico
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class IndicadorEconomico(BaseModel):
    nombre: str
    valor: float | None
    unidad: str
    disponible: bool
    puntos: float
    peso: float
    puntos_ponderados: float


"""
DTOS de RiesgoEconomico
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class RiesgoEconomico(BaseModel):
    score: float
    nivel: str
    recomendacion: str
    puntos_bucket: int
    indicadores: list[IndicadorEconomico]

"""
DTOS de RiesgoProveedorResponse
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class RiesgoProveedorResponse(BaseModel):
    pais: PaisInfo
    riesgo_geopolitico: RiesgoGeopolitico
    riesgo_economico: RiesgoEconomico
    score_total: int
    nivel_combinado: str

"""
DTOS de HistorialItem
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class HistorialItem(BaseModel):
    pais_alpha2: str
    pais_alpha3: str
    pais_nombre: str
    pais_bandera_url: str | None
    score_total: int
    nivel_combinado: str
    consultado_en: dt.datetime

"""
DTOS de CompareItem
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class CompareItem(BaseModel):
    codigo_solicitado: str
    ok: bool
    error: str | None = None
    pais_nombre: str | None = None
    pais_alpha2: str | None = None
    score_geopolitico: int | None = None
    score_economico: float | None = None
    score_total: int | None = None
    nivel_combinado: str | None = None

"""
DTOS de PaisResumen
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class PaisResumen(BaseModel):
    nombre: str
    codigo_alfa2: str
