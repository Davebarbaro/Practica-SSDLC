from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import SQLModel, create_engine, Session, select
from app.models.user import User
from app.models.schemas import UserOut
from app.core.security import require_role, get_current_user
from pathlib import Path
import os
import logging


# Configuración de logging

logger = logging.getLogger(__name__) # Configuramos el logger para este módulo, usando el nombre del módulo actual

# Creamos un router para manejar rutas de usuarios
router = APIRouter()


# Configuración de la base de datos SQLite

current_file = Path(__file__).resolve()                     # Ruta absoluta del archivo actual
project_root = current_file.parent.parent.parent           # Subimos hasta la raííz del proyecto
database_dir = project_root / "database"                   # Carpeta de base de datos
database_path = database_dir / "data.db"                   # Ruta completa del archivo de DB
DATABASE_URL = f"sqlite:///{database_path}"                # URL de conexiónn SQLite
engine = create_engine(DATABASE_URL, echo=False)           # Motor de base de datos


# Ruta para actualizar el rol de un usuario  y solo admin

@router.put("/{user_id}", response_model=UserOut) # Actualiza el rol de un usuario
def update_user_role(
    user_id: int,                                         # ID del usuario en el qie el rol se actualizara
    new_role: str,                                       # Nuevo rol asignado
    admin_user=Depends(require_role("admin"))            # Solo admins pueden ejecutar esta acción
):
    # Actualiza el rol de un usuario específicico, solo admins
    try:
        # 
        # Aqui se crea una lista de roles permitidos y se valida que el nuevo rol esté en esa lista
        #
        ALLOWED_ROLES = ["user", "admin"]
        if new_role not in ALLOWED_ROLES: # Si el rol no es válido, dA error
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid role. Allowed roles: {', '.join(ALLOWED_ROLES)}"
            )
        
        # Validación de ID positivo
        if user_id < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID"
            )
        
      
        # Abrimos sesión de base de datos
       
        with Session(engine) as session:
            # Obtener usuario por ID
            user = session.get(User, user_id)
            
            if not user: # Si el usuario no existe, da errrror
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Guardar  el rol anterior 
            old_role = user.role
            
            # Actualizar rol y guardar cambios en la base de datos
            user.role = new_role
            session.add(user)
            session.commit()
            session.refresh(user)
            
            # Logging de acción crítica y  envia una advertencia al log
            logger.warning(
                f"Admin {admin_user['username']} changed role of user {user.username} "
                f"from {old_role} to {new_role}"
            )
            
            # Devolver usuario actualizado
            return user
            
    except HTTPException:
        # Re-lanzar errores conocidos
        raise
    except Exception as e:
        # Capturar errores inesperados, loguear y devolver error 500
        logger.error(f"Error updating user {user_id} role: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating user"
        )
