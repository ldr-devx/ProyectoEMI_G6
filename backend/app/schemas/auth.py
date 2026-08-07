from pydantic import BaseModel, EmailStr
from app.models.usuario import TipoUsuario


class RegistroRequest(BaseModel):
    email: EmailStr
    password: str
    tipo_usuario: TipoUsuario
    nombre: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    tipo_usuario: str
    user_id: int
    nombre: str
