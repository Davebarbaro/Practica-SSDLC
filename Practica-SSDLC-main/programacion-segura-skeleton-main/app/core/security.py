from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# CARGAR VARIABLES DE ENTORNO DESDE .env
# Busca .env automáticamente en el directorio actual y directorios padres
load_dotenv(override=True)

#
# Se configura la seguridad de la aplicacion en este caso es la gestion de contraseñas y tokens JWT

# SEGURIDAD: La SECRET_KEY debe venir OBLIGATORIAMENTE de las variables de entorno
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError(
        "ERROR CRÍTICO: La variable de entorno 'SECRET_KEY' no está definida. "
        "Por favor, defina SECRET_KEY antes de iniciar la aplicación."
    )

ALGORITHM = os.getenv("ALGORITHM", "HS256")                   # Algoritmo para firmar los tokens
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))  # Expiración token en minutos

# Se configura con que algoritmo se van a hashear las contraseñas

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")  # Usamos Argon2 para proteger contraseñas

# Configuración de OAuth2 para FastAPI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  #Especificamos la url en la que se obtiene los tokens


# Modelo para los datos el caul va usar el token para almacenar informacion del usuario
class TokenData(BaseModel):
    sub: Optional[str] = None  # Nombre de usuario 
    role: Optional[str] = "user"  # Rol del usuario,que  por defecto va a ser "user"


# Funciones para manejar contraseñas
#Esta funcion mira si la contraseña ingreada coincide con el hash guardado en la base de datos
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#Esta otra funcion coje la contraseña y la convierte en un hash seguro para guardar en la base de datos
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Esta funcion crea un token JWT para un usurio 

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None): # Crea un token en el que la data es un diccionario con la informacio del usuario 
                                                                                #y el expires_delta es el tiempo de expiracion del token 
    to_encode = data.copy()  # Copiamos los datos para no modificar el original
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))  # Calculamos expiración, esto se consigue sumando el tiempo actual (utcnow) con el tiempo de expiracion(expires_delta) o otro valor por devefcto
    to_encode.update({"exp": expire})  # Agregamos el campo "exp" al token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Generamos el token firmado a traves de llamar a jwt.encode con los datos, la clave secreta y el algoritmo
    return encoded_jwt 


# Función para obtener el usuario actual desde un token
def get_current_user(token: str = Depends(oauth2_scheme)):  #Obtiene el token de la solicitud gracias o a Depends y oauth2_scheme
    ""
    # Verifica y decodifica el token JWT para obtener la información del usuario, enviado una error si el token no es valido
    credentials_exception = HTTPException( 
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Aqui se descodifica el token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Decodifica el token
        username: str = payload.get("sub")  # Obtenemos el username del token
        role: str = payload.get("role", "user")  # Obtiene el rol, que a no ser que sea el admin sera "user"
        if username is None:
            raise credentials_exception  # Si no hay usuario, suelta un error
        return {"username": username, "role": role}  # Devuelve usuario y rol
    except JWTError:
        raise credentials_exception  # Si ocurre un error al decodificar, lanza excepción

#Funcion que genera una deependecia que solo permite usuarios con un rolo especifico

def require_role(role: str):
    def checker(user = Depends(get_current_user)):  # Usa la funcion get_current_user para obtener el usuario actual
        if user["role"] != role:  # Verifica el rol
            raise HTTPException(status_code=403, detail="Insufficient privileges")  # Error si no coincide
        return user # Devuelve el usuario si el rol coincide
    return checker  # Devuelve la funcion checker 
