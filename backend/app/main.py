import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base
from app.config import settings

# Registrar todos los modelos para que se creen las tablas
import app.models.usuario      # noqa: F401
import app.models.vacante      # noqa: F401
import app.models.postulacion  # noqa: F401
import app.models.certificacion  # noqa: F401
import app.models.notificacion  # noqa: F401

from app.routers import auth, usuarios, vacantes, postulaciones, moderacion, notificaciones, certificaciones

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Plataforma de Empleo USAC",
    description="Bolsa de trabajo segmentada para la comunidad académica de la Facultad de Ingeniería, USAC.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,           prefix="/api/auth",           tags=["Autenticación"])
app.include_router(usuarios.router,       prefix="/api/usuarios",       tags=["Usuarios"])
app.include_router(vacantes.router,       prefix="/api/vacantes",       tags=["Vacantes"])
app.include_router(postulaciones.router,  prefix="/api/postulaciones",  tags=["Postulaciones"])
app.include_router(moderacion.router,     prefix="/api/moderacion",     tags=["Moderación"])
app.include_router(notificaciones.router,    prefix="/api/notificaciones",    tags=["Notificaciones"])
app.include_router(certificaciones.router,  prefix="/api/certificaciones",  tags=["Certificaciones"])

# Servir el frontend como archivos estáticos — debe ir AL FINAL
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", settings.FRONTEND_DIR))
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")
