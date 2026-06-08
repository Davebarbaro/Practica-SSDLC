from sqlmodel import select, Session
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.models.schemas import Token
from app.core.security import verify_password, create_access_token
from app.core.database import get_session


# Router para login de usuarios
router = APIRouter()


# Ruta para login de usuario (OAuth2 con form-data estándar)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    # Buscar usuario por username
    db_user = session.exec(select(User).where(User.username == form_data.username)).first()

    # Verificar que exista y que la contraseña sea correcta
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Crear token JWT con username y rol
    token = create_access_token({"sub": db_user.username, "role": db_user.role})

    # Devolver token y datos del usuario
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": db_user.username,
        "email": db_user.email,
        "role": db_user.role
    }
