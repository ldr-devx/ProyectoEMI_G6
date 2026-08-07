import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class TipoCertificacion(str, enum.Enum):
    propia = "propia"          # Certificación de la plataforma
    afiliado = "afiliado"      # Certificación de empresa aliada


class EstadoCertificacion(str, enum.Enum):
    pendiente = "pendiente"
    verificada = "verificada"
    rechazada = "rechazada"


class Certificacion(Base):
    __tablename__ = "certificaciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo = Column(Enum(TipoCertificacion), nullable=False)
    nombre = Column(String, nullable=False)
    entidad_emisora = Column(String, nullable=False)
    fecha_obtencion = Column(DateTime, nullable=True)
    url_verificacion = Column(String, nullable=True)
    estado = Column(Enum(EstadoCertificacion), default=EstadoCertificacion.pendiente)
    created_at = Column(DateTime, server_default=func.now())

    usuario = relationship("Usuario", back_populates="certificaciones")
