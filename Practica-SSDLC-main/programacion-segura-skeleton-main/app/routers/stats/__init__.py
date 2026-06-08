from fastapi import APIRouter
# Importamos APIRouter para agrupar rutas relacionadas

# Importamos los routers de cada módulo de vulnerabilidades
from .list_vulnerabilities import router as list_router
from .create_vulnerability import router as create_router
from .delete_vulnerability import router as delete_router


# Creamos un router principal para el módulo de vulnerabilidades
router = APIRouter()

# Incluimos los routers de cada funcionalidad
router.include_router(list_router)    # Rutas para listar vulnerabilidades
router.include_router(create_router)  # Rutas para crear vulnerabilidades
router.include_router(delete_router)  # Rutas para eliminar vulnerabilidades
