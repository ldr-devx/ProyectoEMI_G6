from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.certificacion import TipoCertificacion, EstadoCertificacion


class CrearCertificacion(BaseModel):
    tipo: TipoCertificacion
    nombre: str
    entidad_emisora: str
    fecha_obtencion: Optional[datetime] = None
    url_verificacion: Optional[str] = None


class CertificacionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    tipo: TipoCertificacion
    nombre: str
    entidad_emisora: str
    fecha_obtencion: Optional[datetime]
    url_verificacion: Optional[str]
    estado: EstadoCertificacion
    created_at: Optional[datetime]
