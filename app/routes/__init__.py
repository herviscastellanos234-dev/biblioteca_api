from fastapi import APIRouter

from .autores import router as autores_router
from .libros import router as libros_router

api_router = APIRouter()
api_router.include_router(autores_router)
api_router.include_router(libros_router)
