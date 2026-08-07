from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.vacante import TipoVacante, Modalidad, TipoContrato, EstadoVacante


class CrearVacante(BaseModel):
    tipo: TipoVacante
    puesto: str
    empresa_nombre: str
    carrera_compatible: str
    semestre_minimo: int = 1
    modalidad: Modalidad
    tipo_contrato: TipoContrato
    ubicacion: Optional[str] = None
    descripcion: str
    requisitos: Optional[str] = None
    # Referido
    nota_personal: Optional[str] = None
    enlace_oficial: Optional[str] = None
    # Exclusividad
    solo_plataforma: bool = False
    exclusiva_hasta: Optional[datetime] = None
    nivel_minimo_requerido: str = "pendiente"


class VacanteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tipo: TipoVacante
    publicador_id: int
    puesto: str
    empresa_nombre: str
    carrera_compatible: str
    semestre_minimo: int
    modalidad: Modalidad
    tipo_contrato: TipoContrato
    ubicacion: Optional[str]
    descripcion: str
    requisitos: Optional[str]
    nota_personal: Optional[str]
    enlace_oficial: Optional[str]
    solo_plataforma: bool
    exclusiva_hasta: Optional[datetime]
    nivel_minimo_requerido: str
    estado: EstadoVacante
    created_at: Optional[datetime]
