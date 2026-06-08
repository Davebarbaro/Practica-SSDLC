from fastapi import APIRouter
# Importamos APIRouter para agrupar rutas relacionadas

# Importamos routers de cada módulo de usuarios
from .list_users import router as list_users_router
from .get_user import router as get_user_router
from .update_user_role import router as update_user_role_router
from .delete_user import router as delete_user_router


# Definimos qué routers se pueden importar desde este módulo
__all__ = [
    "list_users_router",
    "get_user_router",
    "update_user_role_router",
    "delete_user_router"
]


# Creamos un router principal para el módulo de usuarios

router = APIRouter()

# Incluimos cada sub-router en el router principal
router.include_router(list_users_router)        # Rutas para listar usuarios
router.include_router(get_user_router)          # Rutas para obtener información de un usuario
router.include_router(update_user_role_router)  # Rutas para actualizar el rol de un usuario
router.include_router(delete_user_router)       # Rutas para eliminar un usuario
