from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.postulacion import EstadoPostulacion


class CrearPostulacion(BaseModel):
    vacante_id: int


class ActualizarEstadoPostulacion(BaseModel):
    estado: EstadoPostulacion
    nota_empresa: Optional[str] = None


class PostulacionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    estudiante_id: int
    vacante_id: int
    estado: EstadoPostulacion
    nota_empresa: Optional[str]
    created_at: Optional[datetime]
