from fastapi import APIRouter
# Importamos APIRouter para agrupar rutas relacionadas

# Importamos los routers de cada módulo de mensajes
from .create_message import router as create_router
from .list_messages import router as list_router
from .delete_message import router as delete_router


# Creamos un router principal para el módulo de mensajes
router = APIRouter()

# Incluimos los routers de cada funcionalidad
router.include_router(create_router)  # Rutas para crear mensajes
router.include_router(list_router)    # Rutas para listar mensajes
router.include_router(delete_router)  # Rutas para eliminar mensajes
