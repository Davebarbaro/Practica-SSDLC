from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models.user import Message, User
from app.models.schemas import MessageOut
from app.core.security import get_current_user
from app.core.database import get_session


# Router para listar mensajes
router = APIRouter()


# Ruta para listar los mensajes del usuario actual

@router.get("/", response_model=list[MessageOut])  # Indica que devuelve una lista de MessageOut
def list_my_messages(user=Depends(get_current_user), session: Session = Depends(get_session)):  # Funcion que recibe el usuario actual y una sesión de DB
    # Obtenemos el usuario actual desde el tocken
    db_user = session.exec(select(User).where(User.username == user["username"])).first()

    # Obtenemos todos los mensajes creados por este usuario
    msgs = session.exec(select(Message).where(Message.owner_id == db_user.id)).all()

    return msgs           # Devsolvemos la lista de mensajes
