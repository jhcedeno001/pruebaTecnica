from fastapi import APIRouter

from app.api.endpoints import riesgo_proveedor

api_router = APIRouter()
api_router.include_router(riesgo_proveedor.router)
