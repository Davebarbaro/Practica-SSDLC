from pydantic import BaseModel
from sqlmodel import select, Session
from fastapi import APIRouter, HTTPException, Depends
from app.models.user import User
from app.models.schemas import UserCreate
from app.core.security import get_password_hash, create_access_token
from app.core.database import get_session


# Router para registro de usuarios
router = APIRouter()


# Ruta para registrar un nuevo usuario

@router.post("/register", status_code=201)
def register(user: UserCreate, session: Session = Depends(get_session)):  # Funcion que recibe un UserCreate y una sesipn de DB
    # Verificar si el username ya existe
    exists = session.exec(select(User).where(User.username == user.username)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Username already registered") # Si ya existe, lanzamos un error 400

    # Verificar si el email ya existe
    exists_email = session.exec(select(User).where(User.email == user.email)).first()
    if exists_email:
        raise HTTPException(status_code=400, detail="Email already registered") #  Si ya exist, lanzamos un error 400

    # Crear el usuario con la contraseña hasheada
    db_user = User(
        username=user.username, # Asignamos el username llamando al atributo username del modelo User
        hashed_password=get_password_hash(user.password), # Hasheamos la contraseña
        email=user.email # Asignamos el email llamando al atributo email del modelo User
    )
    session.add(db_user)    # Agregar a la sesion
    session.commit()        # Guardar cambios en la DB
    session.refresh(db_user)  # Actualizar el objeto con datos de la DB

    # Crear token JWT para login automatico después del registro
    token = create_access_token({"sub": db_user.username, "role": db_user.role})

    # Devolver datos al frontend (igual que login)
    return {
        "success": True,
        "access_token": token,
        "token_type": "bearer",
        "user_id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
        "role": db_user.role
    }
