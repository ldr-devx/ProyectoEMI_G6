from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.database import get_db
from app.models.vacante import Vacante, EstadoVacante
from app.models.usuario import Usuario, TipoUsuario
from app.models.notificacion import Notificacion, TipoNotificacion
from app.schemas.vacante import VacanteResponse
from app.core.deps import require_role

router = APIRouter()


class DecisionModeracion(BaseModel):
    accion: str  # "aprobar" | "rechazar"
    motivo: str = ""


@router.get("/cola", response_model=List[VacanteResponse])
def cola_pendiente(
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_role("moderador")),
):
    return db.query(Vacante).filter(Vacante.estado == EstadoVacante.pendiente).order_by(Vacante.created_at.asc()).all()


@router.get("/historial", response_model=List[VacanteResponse])
def historial_moderacion(
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_role("moderador")),
):
    return db.query(Vacante).filter(
        Vacante.estado.in_([EstadoVacante.aprobada, EstadoVacante.rechazada])
    ).order_by(Vacante.created_at.desc()).limit(50).all()


@router.put("/vacantes/{vacante_id}", response_model=VacanteResponse)
def moderar_vacante(
    vacante_id: int,
    decision: DecisionModeracion,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_role("moderador")),
):
    vacante = db.query(Vacante).filter(Vacante.id == vacante_id).first()
    if not vacante:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")

    if decision.accion == "aprobar":
        vacante.estado = EstadoVacante.aprobada
        db.commit()

        # Notificar a estudiantes compatibles
        estudiantes = db.query(Usuario).filter(
            Usuario.tipo_usuario == TipoUsuario.estudiante,
            Usuario.carrera == vacante.carrera_compatible,
            Usuario.semestre >= vacante.semestre_minimo,
        ).all()
        for est in estudiantes:
            db.add(Notificacion(
                usuario_id=est.id,
                tipo=TipoNotificacion.vacante_compatible,
                titulo=f"Nueva vacante: {vacante.puesto}",
                mensaje=f"{vacante.empresa_nombre} publicó una vacante compatible con tu carrera.",
                referencia_id=vacante.id,
            ))
        # Notificar al publicador
        db.add(Notificacion(
            usuario_id=vacante.publicador_id,
            tipo=TipoNotificacion.vacante_aprobada,
            titulo="Tu vacante fue aprobada",
            mensaje=f'"{vacante.puesto}" ya está visible en el feed de estudiantes.',
            referencia_id=vacante.id,
        ))

    elif decision.accion == "rechazar":
        vacante.estado = EstadoVacante.rechazada
        db.commit()

        db.add(Notificacion(
            usuario_id=vacante.publicador_id,
            tipo=TipoNotificacion.vacante_rechazada,
            titulo="Tu vacante fue rechazada",
            mensaje=f'"{vacante.puesto}" no fue aprobada.{" Motivo: " + decision.motivo if decision.motivo else ""}',
            referencia_id=vacante.id,
        ))
    else:
        raise HTTPException(status_code=400, detail="Acción inválida: usa 'aprobar' o 'rechazar'")

    db.commit()
    db.refresh(vacante)
    return vacante
