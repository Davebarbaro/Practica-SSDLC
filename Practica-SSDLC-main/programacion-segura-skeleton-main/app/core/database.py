
# Archivo que configura la base de datos y crea un usuario admin por defecto
from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session, select
from app.models.user import User
from app.models.vulnerability import Vulnerability
from app.core.security import get_password_hash
import os


# Definir la ruta de la base de datos

current_file = Path(__file__).resolve()            # Esta es la ruta actual del archivo database.py
project_root = current_file.parent.parent         # Aqui vamos a la carpeta raíz del proyecto
database_dir = project_root / "database"          # Aqui decimos donde estara la carpeta de la vase de datos
database_dir.mkdir(exist_ok=True)                 # Crea la carpeta si no existe
database_path = database_dir / "data.db"          # Ruta final de la base de datos

DATABASE_URL = f"sqlite:///{database_path}"       # URL de conexión SQLite
print(f" Base de datos: {database_path}")         # Muestra la ruta en consola


# Se crea el engine que permite conectarse a la base de datos 

engine = create_engine(DATABASE_URL, echo=True)   # Con el True vemos las consultas SQL, este engine sirve para conectarnos a la DB

#Es una funcion que inicializa la base de datos creando las tablas y el admin por defecto
def init_db():

    # Verificar si la tabla vulnerability existe y tiene el esquema correcto
    from sqlalchemy import inspect, text
    inspector = inspect(engine)

    if 'vulnerability' in inspector.get_table_names():
        # Verificar si tiene la columna created_at
        columns = [col['name'] for col in inspector.get_columns('vulnerability')]
        if 'created_at' not in columns:
            print("  Tabla 'vulnerability' encontrada sin columna 'created_at'. Recreando tabla...")
            # Borrar la tabla vieja
            with engine.begin() as conn:
                conn.execute(text("DROP TABLE IF EXISTS vulnerability"))
            print(" Tabla 'vulnerability' eliminada correctamente")

    SQLModel.metadata.create_all(engine)          # Crea las tablas que definimos en los modelos
    create_default_admin()                         # Crea un admin por defecto si no existe

# Se crea el usuario admin por defeto
def create_default_admin():

    # SEGURIDAD: La contraseña del admin debe venir de variables de entorno
    admin_password = os.getenv("ADMIN_PASSWORD")
    if not admin_password:
        raise ValueError(
            "ERROR CRÍTICO: La variable de entorno 'ADMIN_PASSWORD' no está definida. "
            "Por favor, defina ADMIN_PASSWORD antes de iniciar la aplicación."
        )

    with Session(engine) as session:             # Abrimos una sesión con la DB
        # Mirar si ya existe un usuario admin
        admin = session.exec(select(User).where(User.username == "admin")).first()

        if not admin:
            # Crear nuevo admin
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash(admin_password),
                role="admin"
            )
            session.add(admin_user)
            session.commit()
            print(" Admin creado: usuario='admin'. La contraseña se cargó desde variables de entorno.")
        else:
            # Actualizar contraseña del admin existente con la del .env
            admin.hashed_password = get_password_hash(admin_password)
            session.add(admin)
            session.commit()
            print(" Contraseña del admin actualizada desde variables de entorno.")

# Funcion para obtner una sesion de la base de datos
def get_session():
    with Session(engine) as session:             # Crea una sesión
        yield session                             # el yield permite usar esta funcion como un generador de sesiones


# NOTA: init_db() se llama desde main.py con @app.on_event("startup")
# No llamar aquí para evitar ejecución duplicada
