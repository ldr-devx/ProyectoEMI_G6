from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.postulacion import Postulacion
from app.models.vacante import Vacante, EstadoVacante
from app.models.usuario import Usuario
from app.models.notificacion import Notificacion, TipoNotificacion
from app.schemas.postulacion import CrearPostulacion, ActualizarEstadoPostulacion, PostulacionResponse
from app.core.deps import get_current_user, require_role

router = APIRouter()


@router.post("/", response_model=PostulacionResponse, status_code=201)
def postular(
    data: CrearPostulacion,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("estudiante")),
):
    vacante = db.query(Vacante).filter(Vacante.id == data.vacante_id, Vacante.estado == EstadoVacante.aprobada).first()
    if not vacante:
        raise HTTPException(status_code=404, detail="Vacante no disponible")

    existente = db.query(Postulacion).filter(
        Postulacion.estudiante_id == current_user.id,
        Postulacion.vacante_id == data.vacante_id,
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya postulaste a esta vacante")

    postulacion = Postulacion(estudiante_id=current_user.id, vacante_id=data.vacante_id)
    db.add(postulacion)
    db.commit()
    db.refresh(postulacion)
    return postulacion


@router.get("/mis-postulaciones", response_model=List[PostulacionResponse])
def mis_postulaciones(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("estudiante")),
):
    return db.query(Postulacion).filter(Postulacion.estudiante_id == current_user.id).order_by(Postulacion.created_at.desc()).all()


@router.get("/vacante/{vacante_id}", response_model=List[PostulacionResponse])
def postulaciones_por_vacante(
    vacante_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("empresa")),
):
    vacante = db.query(Vacante).filter(Vacante.id == vacante_id).first()
    if not vacante:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")
    if vacante.publicador_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes ver candidatos de esta vacante")
    return db.query(Postulacion).filter(Postulacion.vacante_id == vacante_id).order_by(Postulacion.created_at.desc()).all()


@router.put("/{postulacion_id}/estado", response_model=PostulacionResponse)
def actualizar_estado(
    postulacion_id: int,
    data: ActualizarEstadoPostulacion,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("empresa")),
):
    postulacion = db.query(Postulacion).filter(Postulacion.id == postulacion_id).first()
    if not postulacion:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")

    if postulacion.vacante.publicador_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes modificar esta postulación")

    postulacion.estado = data.estado
    if data.nota_empresa:
        postulacion.nota_empresa = data.nota_empresa
    db.commit()

    ESTADO_LABELS = { "en_revision": "En revisión", "aceptada": "Aceptada", "rechazada": "Rechazada", "enviada": "Enviada" }
    db.add(Notificacion(
        usuario_id=postulacion.estudiante_id,
        tipo=TipoNotificacion.cambio_estado_postulacion,
        titulo="Tu postulación fue actualizada",
        mensaje=f'Tu postulación a "{postulacion.vacante.puesto}" cambió a: {ESTADO_LABELS.get(data.estado, data.estado)}.',
        referencia_id=postulacion.id,
    ))
    db.commit()
    db.refresh(postulacion)
    return postulacion
