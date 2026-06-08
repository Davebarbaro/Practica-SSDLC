from fastapi import APIRouter
# Importamos APIRouter para agrupar rutas relacionadas

# Importamos los routers de cada módulo de autenticación
from .register import router as register_router
from .login import router as login_router


# Creamos un router principal para el módulo de autenticación
router = APIRouter()

# Incluimos los routers de cada funcionalidad
router.include_router(register_router)  # Rutas para registro de usuarios
router.include_router(login_router)     # Rutas para login de usuarios

