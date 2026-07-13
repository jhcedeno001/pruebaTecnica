from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.db.catalog_seeder import seed_pais_catalogo
from app.db.schema_initializer import SchemaInitializer
from app.db.session import engine
from app.models import riesgo_proveedor  # noqa: F401 - registra los modelos en Base.metadata

"""
Creación de tablas y registro de catalogo al inicar el servicio
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await SchemaInitializer(engine).crear_tablas()
    await seed_pais_catalogo()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    return app


app = create_app()
