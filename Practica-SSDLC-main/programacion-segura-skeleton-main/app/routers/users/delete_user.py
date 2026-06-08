from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import SQLModel, create_engine, Session, select
from app.models.user import User
from app.models.schemas import UserOut
from app.core.security import require_role, get_current_user
from pathlib import Path
import os
import logging


# Configuración de logging

logger = logging.getLogger(__name__)# Configuramos el logger para este módulo, usando el nombre del módulo actual 


# Creamos un router para manejar rutas de usuarios

router = APIRouter()


# Configuración de la base de datos SQLite

current_file = Path(__file__).resolve()                     # Ruta absoluta del archivo actual
project_root = current_file.parent.parent.parent           # Subimos hasta la raíz del proyecto
database_dir = project_root / "database"                   # Carpeta donde se encuentra la DB
database_path = database_dir / "data.db"                   # Ruta completa del archivo de DB
DATABASE_URL = f"sqlite:///{database_path}"                # URL de conexión SQLite
engine = create_engine(DATABASE_URL, echo=False)           # Motor de base de datos, echo=False oculta SQL en consola


# Ruta para eliminar un usuario (solo Admin)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_user(
    user_id: int,  # ID del usuario a eliminar
    admin_user=Depends(require_role("admin"))               # Solo admins pueden ejecutar esta función
):
   
    #elimina un usuario por su ID, asegurando que el admin no pueda eliminarse a sí mismo.

    try:
    
        # Validación de entrada hacieendo que el id debe ser positivo  si no es así devuelve un error
        
        if user_id < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID"
            )
        
        #
        # Abrimos sesión de base de datos
      
        with Session(engine) as session:
            # Obtener usuario a eliminar
            user = session.get(User, user_id)
            # Si el usuario no existe, devolver error 404
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Obtener información del admin que realiza la acción
            admin = session.exec(
                select(User).where(User.username == admin_user["username"])
            ).first()
            
            # Prevenir que el admin se elimine a sí mismo
            if admin.id == user_id: 
                logger.warning(f"Admin {admin_user['username']} attempted self-deletion") # Logueamos el intento de auto-eliminación, enviando una advertencia
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot delete your own account"
                )
            
            # Guardar información antes de eliminar para logging
            deleted_username = user.username
            
            # Eliminar usuario
            session.delete(user)
            session.commit()
            
            # Logging de operación crítica
            logger.warning(
                f"Admin {admin_user['username']} deleted user {deleted_username} (ID: {user_id})" # Logueamos la eliminación del usuario por parte del admin
            )
            
            return None  # 204 No Content
            
    except HTTPException:
        # Re-lanzamos errores conocidos (400, 404)
        raise
    except Exception as e:
        # Capturamos errores inesperados y devolvemos 500
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting user"
        )
