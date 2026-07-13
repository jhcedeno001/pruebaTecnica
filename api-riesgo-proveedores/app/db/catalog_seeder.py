import logging

from app.clients.referencia_geografica_client import ReferenciaGeograficaClient
from app.db.session import SessionLocal
from app.repositories.pais_catalogo_repository import PaisCatalogoRepository

logger = logging.getLogger(__name__)

"""
Metodo encargado de llenar el catalogo de paises
@Author jhcedeno<jose22ced@gmail.com>
@Version 1.0
"""
async def seed_pais_catalogo() -> None:
    async with SessionLocal() as session:
        repositorio = PaisCatalogoRepository(session)
        if await repositorio.existe_alguno():
            return

        async with ReferenciaGeograficaClient() as client:
            catalogo = await client.get_catalogo_paises()

        if not catalogo:
            logger.warning("No se puedo otener el catalogo de paises")
            return

        await repositorio.insertar_todos(catalogo)
        await session.commit()
        logger.info("Catalogo", len(catalogo))
