from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime
from app.models.usuario import TipoUsuario, NivelVerificacion, EstadoAcademico


class UsuarioPublico(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: Optional[str]
    tipo_usuario: TipoUsuario
    nivel_verificacion: NivelVerificacion
    carrera: Optional[str]
    escuela: Optional[str]
    semestre: Optional[int]
    creditos_aprobados: Optional[int]
    estado_academico: Optional[EstadoAcademico]
    bio: Optional[str]
    github_url: Optional[str]
    portfolio_url: Optional[str]
    nombre_empresa: Optional[str]
    sector: Optional[str]
    sitio_web: Optional[str]


class UsuarioMe(UsuarioPublico):
    email: str
    telefono: Optional[str]
    cv_url: Optional[str]
    carrera_egresada: Optional[str]
    created_at: Optional[datetime]


class ActualizarPerfil(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    # Estudiante
    carrera: Optional[str] = None
    escuela: Optional[str] = None
    semestre: Optional[int] = None
    creditos_aprobados: Optional[int] = None
    estado_academico: Optional[EstadoAcademico] = None
    bio: Optional[str] = None
    cv_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    # Empresa
    nombre_empresa: Optional[str] = None
    sector: Optional[str] = None
    sitio_web: Optional[str] = None
    # Referidor
    carrera_egresada: Optional[str] = None
