from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.auth import RegistroRequest, LoginRequest, TokenResponse
from app.core.security import verify_password, get_password_hash, create_access_token

router = APIRouter()


@router.post("/registro", response_model=TokenResponse, status_code=201)
def registro(data: RegistroRequest, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == data.email).first():
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    user = Usuario(
        email=data.email,
        password_hash=get_password_hash(data.password),
        tipo_usuario=data.tipo_usuario,
        nombre=data.nombre,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({
        "sub": user.email,
        "user_id": user.id,
        "tipo_usuario": user.tipo_usuario.value,
    })
    return TokenResponse(
        access_token=token,
        tipo_usuario=user.tipo_usuario.value,
        user_id=user.id,
        nombre=user.nombre or "",
    )


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Cuenta inactiva")

    token = create_access_token({
        "sub": user.email,
        "user_id": user.id,
        "tipo_usuario": user.tipo_usuario.value,
    })
    return TokenResponse(
        access_token=token,
        tipo_usuario=user.tipo_usuario.value,
        user_id=user.id,
        nombre=user.nombre or "",
    )
