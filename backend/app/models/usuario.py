import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, func
from sqlalchemy.orm import relationship
from app.database import Base


class TipoUsuario(str, enum.Enum):
    estudiante = "estudiante"
    empresa = "empresa"
    referidor = "referidor"
    moderador = "moderador"


class NivelVerificacion(str, enum.Enum):
    pendiente = "pendiente"
    basico = "basico"
    certificado = "certificado"
    verificado = "verificado"


class EstadoAcademico(str, enum.Enum):
    activo = "activo"
    eps = "eps"
    graduado = "graduado"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    tipo_usuario = Column(Enum(TipoUsuario), nullable=False)
    nivel_verificacion = Column(Enum(NivelVerificacion), default=NivelVerificacion.pendiente)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    # Campos comunes a todos los roles
    nombre = Column(String, nullable=True)
    telefono = Column(String, nullable=True)

    # Solo estudiante/egresado
    carrera = Column(String, nullable=True)
    escuela = Column(String, nullable=True)
    semestre = Column(Integer, nullable=True)
    creditos_aprobados = Column(Integer, nullable=True)
    estado_academico = Column(Enum(EstadoAcademico), nullable=True)
    bio = Column(String, nullable=True)
    cv_url = Column(String, nullable=True)
    github_url = Column(String, nullable=True)
    portfolio_url = Column(String, nullable=True)

    # Solo empresa
    nombre_empresa = Column(String, nullable=True)
    sector = Column(String, nullable=True)
    sitio_web = Column(String, nullable=True)

    # Solo referidor
    carrera_egresada = Column(String, nullable=True)

    vacantes_publicadas = relationship("Vacante", back_populates="publicador", cascade="all, delete-orphan")
    postulaciones = relationship("Postulacion", back_populates="estudiante", cascade="all, delete-orphan")
    certificaciones = relationship("Certificacion", back_populates="usuario", cascade="all, delete-orphan")
    notificaciones = relationship("Notificacion", back_populates="usuario", cascade="all, delete-orphan")
