from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.user import Message, User
from app.models.schemas import MessageCreate, MessageOut
from app.core.security import get_current_user
from app.core.database import get_session


# Router para crear mensajes
router = APIRouter()


# Ruta para crear un nuevo mensaje

@router.post("/", response_model=MessageOut, status_code=201)  # Indica que devuelve un MessageOut y código 201
def create_message(payload: MessageCreate, user=Depends(get_current_user), session: Session = Depends(get_session)): # Funcion que recibe un MessageCreate, el usuario actual y una sesion de DB
    # Obtenemos el usuario actual desde el token( el exec indica ejecutar una consulta a la base de datos y el session es la conexion a la base de datos)
    db_user = session.exec(select(User).where(User.username == user["username"])).first()

    # Creamos un mensaje en el que el owner_id es  id del usuario actual y el contenido es el que viene en el payload
    msg = Message(content=payload.content, owner_id=db_user.id)

    session.add(msg)      # Agregamos el mensaje a la sesion
    session.commit()      # Guardamo cambios en la base de datos
    session.refresh(msg)  # Refrescamos el objeto para obtener ID generado

    return msg            # Devolvemos el mensaje creado
