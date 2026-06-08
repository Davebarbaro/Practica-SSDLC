from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import SQLModel, create_engine, Session, select
from app.models.user import User
from app.models.schemas import UserOut
from app.core.security import require_role, get_current_user
from pathlib import Path
import os
import logging

# Configuración de logging

logger = logging.getLogger(__name__) # Configuraamos el logger paroa este modulo, usando el nombre del módulo actual


# Creamos un router para manejar rutas de usuarios

router = APIRouter()


# Configuración de la base de datos SQLite

current_file = Path(__file__).resolve()                     # Ruta absoluta del archivo actual
project_root = current_file.parent.parent.parent           # Subimos hasta la raz del proyecto
database_dir = project_root / "database"                   # Carpeta de base de datos
database_path = database_dir / "data.db"                   # Ruta completa del archivo de DB
DATABASE_URL = f"sqlite:///{database_path}"                # URL de conexion SQLite
engine = create_engine(DATABASE_URL, echo=False)           # Motor de base de datos


# Ruta para listar usuarios con numeración (solo Admin)

@router.get("/", response_model=list[UserOut]) # Lista de usuarios
def list_users(
    skip: int = 0,                                         # Pagina de inicio
    limit: int = 100,                                      # Número máximo de registros a devolver
    user=Depends(require_role("admin"))                     # Solo admins pueden ejecutar esta ruta
):
    # Lista usuarios con paginación, solo accesible para adminss
    try:
       
        # Validación de parámetros de paginación
        
        if skip < 0 or limit < 1 or limit > 100: # Limitar el maximo a 100 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid pagination parameters"
            )
        
        
        # Abrimos sesión de base de datos
        
        with Session(engine) as session:
            # Obtener usuarios con paginación
            users = session.exec(
                select(User).offset(skip).limit(limit)
            ).all()
            
            # Logging de acción crítica
            logger.info(f"Admin {user['username']} listed users (skip={skip}, limit={limit})")
            
            return users  # Devolver lista de usuarios
            
    except HTTPException:
        # Re-lanzar errores conocidos
        raise
    except Exception as e:
        # Capturar errores inesperados, loguear y devolver error 500
        logger.error(f"Error listing users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving users"
        )
