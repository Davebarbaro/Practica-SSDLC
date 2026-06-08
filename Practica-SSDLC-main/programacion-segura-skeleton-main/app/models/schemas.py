from pydantic import BaseModel, Field, EmailStr
# Importamos BaseModel de Pydantic para crear modelos de datos
# Field nos permite añadir validaciones y metadatos a los campos
# EmailStr ve que un string sea un email válido


# Modelo para crear un usuario

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)  # Nombre de usuario, 3-50 caracteres
    password: str = Field(min_length=8, max_length=128) # Contraseña, 8-128 caracteres
    email: EmailStr = Field(...)                        # Email obligatorio gracias a EmailStr

# 
# Modelo para devolver información de usuario

class UserOut(BaseModel):
    id: int          # ID del usuario en la base de datos
    username: str    # Nombre de usuario
    role: str        # Rol del usuario 

    class Config:
        from_attributes = True  # Permite crear este modelo a partir de objetos ORM (de la base de datos)


# Modelo para devolver token de acceso

class Token(BaseModel):
    access_token: str  # Token JWT
    token_type: str = "bearer"  # Tipo de token, por defecto "bearer", esto es estándar en OAuth2, el beaber dice que el token debe ser enviado en el header Authorization
    username: str      # Nombre de usuario correspondiente al token
    email: str         # Email del usuario
    role: str          # Rol del usuario

#
# Modelo para crear un mensaje

class MessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=500)  # Contenido del mensaje, mínimo 1 carácter, máximo 500


# Modelo para devolver un mensaje

class MessageOut(BaseModel):
    id: int          # ID del mensaje
    content: str     # Contenido del mensaje
    owner_id: int    # ID del usuario que creó el mensaje

    class Config:
        from_attributes = True  # Permite crear este modelo a partir de objetos ORM (de la base de datos
