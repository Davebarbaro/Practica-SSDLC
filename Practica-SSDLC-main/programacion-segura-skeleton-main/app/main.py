from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
from app.routers.messages import router as messages_router
from app.routers.users import router as users_router
from app.routers.stats import router as stats_router
from app.core.database import init_db

# Creamos la aplicacion FastAPI

app = FastAPI(title="Secure API Starter")


# Inicializar la base de datos al iniciar la app

@app.on_event("startup")
def on_startup():
    init_db()  # Crea tablas y usuario admin si no existe


# Configuración de CORS (Cross-Origin Resource Sharing) para permitir solicitudes desde orígenes específicos
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8001",
        "http://127.0.0.1:8001",
        "http://localhost:8080",
        "https://localhost:8443",
        "http://127.0.0.1:8080",
        "https://127.0.0.1:8443"
    ],                       # OAqui estan los orígenes permitidos
    allow_credentials=True,   # Permitir envío de cookies y credenciales
    allow_methods=["*"],      # Permitir todos los métodos HTTP
    allow_headers=["*"],      # Permitir todos los headers
)


# Endpoint de helth 

@app.get("/health")
def health():
    return {"status": "ok"}  # Devuelve un JSON sque indica que la API funciona bien


# Incluir routers para las diferentes funcionalidaddes
#
app.include_router(auth_router, prefix="/auth", tags=["auth"])                       # Rutas de autenticación
app.include_router(users_router, prefix="/users", tags=["users"])                   # Rutas de usuarios
app.include_router(messages_router, prefix="/messages", tags=["messages"])          # Rutas de mensajes
app.include_router(stats_router, prefix="/stats/vulnerabilidades", tags=["vulnerabilities"])  # Rutas devulnerabilidades
