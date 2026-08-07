import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class TipoVacante(str, enum.Enum):
    empresa = "empresa"
    referido = "referido"


class Modalidad(str, enum.Enum):
    presencial = "presencial"
    remoto = "remoto"
    hibrido = "hibrido"


class TipoContrato(str, enum.Enum):
    tiempo_completo = "tiempo_completo"
    medio_tiempo = "medio_tiempo"
    practica = "practica"
    freelance = "freelance"


class EstadoVacante(str, enum.Enum):
    pendiente = "pendiente"
    aprobada = "aprobada"
    rechazada = "rechazada"


class Vacante(Base):
    __tablename__ = "vacantes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(TipoVacante), nullable=False)
    publicador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    puesto = Column(String, nullable=False)
    empresa_nombre = Column(String, nullable=False)
    carrera_compatible = Column(String, nullable=False)
    semestre_minimo = Column(Integer, default=1)
    modalidad = Column(Enum(Modalidad), nullable=False)
    tipo_contrato = Column(Enum(TipoContrato), nullable=False)
    ubicacion = Column(String, nullable=True)
    descripcion = Column(String, nullable=False)
    requisitos = Column(String, nullable=True)

    # Solo para referidos
    nota_personal = Column(String, nullable=True)
    enlace_oficial = Column(String, nullable=True)

    # Modelo de negocio: exclusividad
    solo_plataforma = Column(Boolean, default=False)
    exclusiva_hasta = Column(DateTime, nullable=True)
    nivel_minimo_requerido = Column(String, default="pendiente")

    estado = Column(Enum(EstadoVacante), default=EstadoVacante.pendiente)
    created_at = Column(DateTime, server_default=func.now())

    publicador = relationship("Usuario", back_populates="vacantes_publicadas")
    postulaciones = relationship("Postulacion", back_populates="vacante", cascade="all, delete-orphan")
