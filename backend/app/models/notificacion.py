import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class TipoNotificacion(str, enum.Enum):
    vacante_compatible = "vacante_compatible"
    cambio_estado_postulacion = "cambio_estado_postulacion"
    vacante_aprobada = "vacante_aprobada"
    vacante_rechazada = "vacante_rechazada"
    otro = "otro"


class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo = Column(Enum(TipoNotificacion), nullable=False)
    titulo = Column(String, nullable=False)
    mensaje = Column(String, nullable=False)
    leida = Column(Boolean, default=False)
    referencia_id = Column(Integer, nullable=True)  # vacante_id o postulacion_id
    created_at = Column(DateTime, server_default=func.now())

    usuario = relationship("Usuario", back_populates="notificaciones")
