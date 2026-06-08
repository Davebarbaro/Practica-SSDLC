from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import SQLModel, create_engine, Session, select
from app.models.user import User
from app.models.schemas import UserOut
from app.core.security import require_role, get_current_user
from pathlib import Path
import os
import logging

# Configuración de logging
logger = logging.getLogger(__name__)  # Configuramos el logger para este módulo, usando el nombre del módulo actual


# Creamos un router para manejar rutas de usuarios

router = APIRouter()


# Configuración de la base de datos SQLite

current_file = Path(__file__).resolve()                     # Ruta absoluta del archivo actual
project_root = current_file.parent.parent.parent           # Subimos hasta la raíz del proyecto
database_dir = project_root / "database"                   # Carpeta de base de datos
database_path = database_dir / "data.db"                   # Ruta completa del archivo de DB
DATABASE_URL = f"sqlite:///{database_path}"                # URL de conexión SQLite
engine = create_engine(DATABASE_URL, echo=False)           # Motor de base de datos


# Ruta para obtener información de un usuario específico

@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,                                         # ID del usuario solicitado
    current_user=Depends(get_current_user)               # Usuario autenticado desde token
):
   # Obtiene información de un usuario por su id ademas de tener un  control de acceso para admin 
    try:
      
        # Validación de entrada: ID positivo ya que no existen IDs negativos 
        
        if user_id < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID"
            )
        
        
        # Abrimos sesión de base de datos
       
        with Session(engine) as session:
            # Obtener el usuario solicitado
            target_user = session.get(User, user_id)
            
            if not target_user:
                # Mismo mensaje para evitar enumeración de usuarios
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Obtener usuario actual para verificar ownership 
            db_current_user = session.exec(
                select(User).where(User.username == current_user["username"])
            ).first()
            
    
            # Aqui se implementa el control de acceso
           
            if current_user["role"] != "admin" and db_current_user.id != user_id: # Solo admin o el mismo usuario pueden acceder
                logger.warning(
                    f"User {current_user['username']} attempted unauthorized access to user {user_id}"
                )
                raise HTTPException(  # 403 Forbidddenn si no tiene permisos
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient privileges"
                )
            
            # Logging de acceso exitoso
            logger.info(f"User {current_user['username']} accessed user {user_id} details")
            
            # Devolver información del usuario solicitado
            return target_user
            
    except HTTPException:
        # Re-lanzar errores conocidos (400, 404, 403)
        raise
    except Exception as e:
        # Capturar errores inesperados y devolver 500
        logger.error(f"Error retrieving user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving user"
        )
