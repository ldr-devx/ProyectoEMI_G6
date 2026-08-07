from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.models.vacante import Vacante, EstadoVacante
from app.models.usuario import Usuario
from app.schemas.vacante import CrearVacante, VacanteResponse
from app.core.deps import get_current_user, require_role

router = APIRouter()


@router.post("/", response_model=VacanteResponse, status_code=201)
def publicar_vacante(
    data: CrearVacante,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("empresa", "referidor")),
):
    vacante = Vacante(**data.model_dump(), publicador_id=current_user.id)
    db.add(vacante)
    db.commit()
    db.refresh(vacante)
    return vacante


@router.get("/", response_model=List[VacanteResponse])
def listar_vacantes(
    carrera: Optional[str] = Query(None),
    semestre_minimo: Optional[int] = Query(None),
    tipo_contrato: Optional[str] = Query(None),
    tipo: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Vacante).filter(Vacante.estado == EstadoVacante.aprobada)

    if carrera:
        query = query.filter(Vacante.carrera_compatible.ilike(f"%{carrera}%"))
    if semestre_minimo is not None:
        query = query.filter(Vacante.semestre_minimo <= semestre_minimo)
    if tipo_contrato:
        query = query.filter(Vacante.tipo_contrato == tipo_contrato)
    if tipo:
        query = query.filter(Vacante.tipo == tipo)

    return query.order_by(Vacante.created_at.desc()).all()


@router.get("/{vacante_id}", response_model=VacanteResponse)
def detalle_vacante(vacante_id: int, db: Session = Depends(get_db)):
    vacante = db.query(Vacante).filter(Vacante.id == vacante_id).first()
    if not vacante:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")
    return vacante


@router.get("/mis-vacantes/publicadas", response_model=List[VacanteResponse])
def mis_vacantes(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("empresa", "referidor")),
):
    return db.query(Vacante).filter(Vacante.publicador_id == current_user.id).order_by(Vacante.created_at.desc()).all()
