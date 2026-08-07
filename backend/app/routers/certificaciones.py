from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.certificacion import Certificacion, EstadoCertificacion
from app.models.usuario import Usuario, NivelVerificacion
from app.schemas.certificacion import CrearCertificacion, CertificacionResponse
from app.core.deps import get_current_user, require_role

router = APIRouter()


def recalcular_nivel(usuario: Usuario, db: Session):
    certs = db.query(Certificacion).filter(
        Certificacion.usuario_id == usuario.id,
        Certificacion.estado == EstadoCertificacion.verificada,
    ).count()

    if certs >= 3:
        usuario.nivel_verificacion = NivelVerificacion.verificado
    elif certs >= 1:
        usuario.nivel_verificacion = NivelVerificacion.certificado
    else:
        usuario.nivel_verificacion = NivelVerificacion.basico
    db.commit()


@router.post("/", response_model=CertificacionResponse, status_code=201)
def agregar_certificacion(
    data: CrearCertificacion,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("estudiante")),
):
    cert = Certificacion(**data.model_dump(), usuario_id=current_user.id)
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert


@router.get("/mis-certificaciones", response_model=List[CertificacionResponse])
def mis_certificaciones(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("estudiante")),
):
    return db.query(Certificacion).filter(
        Certificacion.usuario_id == current_user.id
    ).order_by(Certificacion.created_at.desc()).all()


@router.get("/pendientes", response_model=List[CertificacionResponse])
def certificaciones_pendientes(
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_role("moderador")),
):
    return db.query(Certificacion).filter(
        Certificacion.estado == EstadoCertificacion.pendiente
    ).order_by(Certificacion.created_at.asc()).all()


@router.put("/{cert_id}/verificar", response_model=CertificacionResponse)
def verificar_certificacion(
    cert_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_role("moderador")),
):
    cert = db.query(Certificacion).filter(Certificacion.id == cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificación no encontrada")
    if cert.estado != EstadoCertificacion.pendiente:
        raise HTTPException(status_code=400, detail="Esta certificación ya fue procesada")

    cert.estado = EstadoCertificacion.verificada
    db.commit()

    usuario = db.query(Usuario).filter(Usuario.id == cert.usuario_id).first()
    if usuario:
        recalcular_nivel(usuario, db)

    db.refresh(cert)
    return cert


@router.put("/{cert_id}/rechazar", response_model=CertificacionResponse)
def rechazar_certificacion(
    cert_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_role("moderador")),
):
    cert = db.query(Certificacion).filter(Certificacion.id == cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificación no encontrada")
    if cert.estado != EstadoCertificacion.pendiente:
        raise HTTPException(status_code=400, detail="Esta certificación ya fue procesada")

    cert.estado = EstadoCertificacion.rechazada
    db.commit()
    db.refresh(cert)
    return cert
