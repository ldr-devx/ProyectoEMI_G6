from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.database import get_db
from app.models.notificacion import Notificacion, TipoNotificacion
from app.models.usuario import Usuario
from app.core.deps import get_current_user

router = APIRouter()


class NotificacionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tipo: TipoNotificacion
    titulo: str
    mensaje: str
    leida: bool
    referencia_id: int | None
    created_at: datetime | None


@router.get("/", response_model=List[NotificacionResponse])
def mis_notificaciones(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return db.query(Notificacion).filter(
        Notificacion.usuario_id == current_user.id
    ).order_by(Notificacion.created_at.desc()).limit(50).all()


@router.put("/{notificacion_id}/leer")
def marcar_leida(
    notificacion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    notif = db.query(Notificacion).filter(
        Notificacion.id == notificacion_id,
        Notificacion.usuario_id == current_user.id,
    ).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    notif.leida = True
    db.commit()
    return {"ok": True}


@router.put("/leer-todas")
def marcar_todas_leidas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    db.query(Notificacion).filter(
        Notificacion.usuario_id == current_user.id,
        Notificacion.leida == False,
    ).update({"leida": True})
    db.commit()
    return {"ok": True}
