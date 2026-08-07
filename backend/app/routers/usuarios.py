from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioMe, UsuarioPublico, ActualizarPerfil
from app.core.deps import get_current_user

router = APIRouter()


@router.get("/me", response_model=UsuarioMe)
def get_mi_perfil(current_user: Usuario = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UsuarioMe)
def actualizar_mi_perfil(
    data: ActualizarPerfil,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/{usuario_id}", response_model=UsuarioPublico)
def get_perfil_publico(usuario_id: int, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.is_active == True).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
