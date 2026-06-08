from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.user import Message, User
from app.core.security import get_current_user
from app.core.database import get_session


# Router para eliminar mensajes
router = APIRouter()


# Ruta para eliminar un mensaje

@router.delete("/{message_id}", status_code=204) # Este mensaje se envia cuando la operacion se ha realizado con exito
def delete_message(message_id: int, user=Depends(get_current_user), session: Session = Depends(get_session)):  # Funcion que recibe el ID del mensaje a eliminar, el usuario actual y una sesión de DB

    # Obtenemos el mensaje por ID
    msg = session.get(Message, message_id)

    # Verificamos que el mensaje exista y que pertenezca al usuario actual
    if not msg or msg.owner_id != session.exec(select(User).where(User.username == user["username"])).first().id:
        raise HTTPException(status_code=404, detail="Message not found") # Si no existe o no pertenece al usuario, sale un error 404

    session.delete(msg)   # Eliminamos el mensaje
    session.commit()      # Guardamos cambios en la DB

    return                 # Retornamos vacío, status_code=204 indica éxito sin contenido
