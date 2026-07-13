import datetime as dt

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

"""
Clase y tabla de Region
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class Region(Base):
    __tablename__ = "region"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True)
    tensiones_diplomaticas: Mapped[bool] = mapped_column(default=False)

    paises: Mapped[list["Pais"]] = relationship(back_populates="region")

"""
Clase y tabla de Moneda
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class Moneda(Base):
    __tablename__ = "moneda"

    id: Mapped[int] = mapped_column(primary_key=True)
    siglas: Mapped[str] = mapped_column(String(10), unique=True)
    nombre: Mapped[str] = mapped_column(String(50))
    tasa_cambio: Mapped[float | None] = mapped_column(default=None)
    actualizado_en: Mapped[dt.datetime | None] = mapped_column(default=None)

    paises: Mapped[list["Pais"]] = relationship(back_populates="moneda")

"""
Clase y tabla de Pais
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class Pais(Base):
    __tablename__ = "pais"

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo_alfa2: Mapped[str] = mapped_column(String(2), unique=True, index=True)
    codigo_alfa3: Mapped[str] = mapped_column(String(3), unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100))
    subregion: Mapped[str | None] = mapped_column(String(50))
    bandera_url: Mapped[str | None] = mapped_column(String(255))
    capital: Mapped[str | None] = mapped_column(String(100))
    poblacion: Mapped[int | None] = mapped_column(default=None)
    area: Mapped[float | None] = mapped_column(default=None)
    poblacion_densidad: Mapped[float | None] = mapped_column(default=None)
    fronteras: Mapped[list[str] | None] = mapped_column(JSON, default=None)

    moneda_id: Mapped[int | None] = mapped_column(ForeignKey("moneda.id"))
    region_id: Mapped[int | None] = mapped_column(ForeignKey("region.id"))

    creado_en: Mapped[dt.datetime] = mapped_column(default=dt.datetime.utcnow)
    actualizado_en: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow
    )

    moneda: Mapped[Moneda | None] = relationship(back_populates="paises")
    region: Mapped[Region | None] = relationship(back_populates="paises")
    detalles: Mapped[list["PaisDetalle"]] = relationship(back_populates="pais")

"""
Clase y tabla de PaisDetalle
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class PaisDetalle(Base):
    __tablename__ = "pais_detalle"

    id: Mapped[int] = mapped_column(primary_key=True)
    pais_id: Mapped[int] = mapped_column(ForeignKey("pais.id"), index=True)

    score_geopolitico: Mapped[int]
    score_economico: Mapped[float]
    variacion_cambiaria: Mapped[float | None] = mapped_column(default=None)
    score_total: Mapped[int]
    nivel_combinado: Mapped[str] = mapped_column(String(20))

    consultado_en: Mapped[dt.datetime] = mapped_column(default=dt.datetime.utcnow, index=True)

    pais: Mapped[Pais] = relationship(back_populates="detalles")


"""
Clase y tabla de PaisCatalogo
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
class PaisCatalogo(Base):
    __tablename__ = "pais_catalogo"

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo_alfa2: Mapped[str] = mapped_column(String(2), unique=True, index=True)
    codigo_alfa3: Mapped[str] = mapped_column(String(3), unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100))
