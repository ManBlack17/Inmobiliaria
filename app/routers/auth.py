from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.models import Usuario
from app.utils import hash_password, verify_password, create_access_token
from pydantic import BaseModel

router = APIRouter(tags=["Autenticación"])

class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    password: str
    rol: str = "usuario"  # Por defecto, los usuarios normales

#class UsuarioLogin(BaseModel):
#    email: str
#    password: str

@router.post("/register")
def register(user: UsuarioCreate, db: Session = Depends(get_db)):
    user_exists = db.query(Usuario).filter(Usuario.email == user.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    hashed_password = hash_password(user.password)
    nuevo_usuario = Usuario(
        nombre=user.nombre, 
        email=user.email, 
        hashed_password=hashed_password, 
        rol=user.rol
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return {
        "id": nuevo_usuario.id,
        "nombre": nuevo_usuario.nombre,
        "email": nuevo_usuario.email,
        "rol": nuevo_usuario.rol,
        "message": "Usuario registrado correctamente"
    }

@router.post("/login")
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Autentica al usuario y devuelve un token de acceso."""
    usuario = db.query(Usuario).filter(Usuario.email == user.username).first()
    if not usuario or not verify_password(user.password, usuario.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    access_token = create_access_token({"sub": str(usuario.id), "rol": usuario.rol})
    return {"access_token": access_token, "token_type": "bearer"}
