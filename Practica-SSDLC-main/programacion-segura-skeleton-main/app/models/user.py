from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
# SQLModel  permte definir modelos de base de datos usando clases de Python
# El Field define las propiedades de cada columna
# Relationship define relaciones entre tablas
# Optional indica que un valor puede ser None
# List indica listas de objetos relacionados

# Modelo de usuario

class User(SQLModel, table=True):  # table=True indica que esta clase es una tabla en la base de datos
    id: Optional[int] = Field(default=None, primary_key=True)  # ID que se autoincrementa automáticamente, es autoincremental porque el default es None entonces
    username: str = Field(index=True, unique=True)              # Nombre de usuario único y con índice 
    email: str = Field(index=True, unique=True)                 # Email único y con índice
    hashed_password: str                                        # Contraseña en hash (no se guarda en texto plano)
    role: str = Field(default="user")                           # Rol del usuario, por defecto "user"
    messages: List["Message"] = Relationship(back_populates="owner")  # Especial atributo que define la relación uno a muchos con mensajes es decir un usuario puede tener muchos mensajes,
    #La estructura del message aqui nos dice que yamara a buscar en la clase Message el atributo owner el cual es el que tiene la relacion inversa, esta relacion inversa hace que desde un usuario podamos acceder a todos sus mensajes



# Modelo de mensaje

class Message(SQLModel, table=True): #
    id: Optional[int] = Field(default=None, primary_key=True)  # ID autoincremental
    content: str                                              # Contenido del mensaje
    owner_id: int = Field(foreign_key="user.id")              # Clave foránea que apunta al usuario, la clave foranea dice que este camoo es uan referncia a la tabla user en su id
    owner: Optional[User] = Relationship(back_populates="messages")  
    # Atibuto que  hace que desde un usuario podamos acceder a todos sus mensajes
