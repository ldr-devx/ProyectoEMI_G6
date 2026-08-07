import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from app.database import Base


class EstadoPostulacion(str, enum.Enum):
    enviada = "enviada"
    en_revision = "en_revision"
    aceptada = "aceptada"
    rechazada = "rechazada"


class Postulacion(Base):
    __tablename__ = "postulaciones"
    __table_args__ = (
        UniqueConstraint("estudiante_id", "vacante_id", name="uq_postulacion"),
    )

    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    vacante_id = Column(Integer, ForeignKey("vacantes.id"), nullable=False)
    estado = Column(Enum(EstadoPostulacion), default=EstadoPostulacion.enviada)
    nota_empresa = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    estudiante = relationship("Usuario", back_populates="postulaciones")
    vacante = relationship("Vacante", back_populates="postulaciones")
