from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.utils import get_current_user

router = APIRouter(tags=["Puntos de Interés"])

# Crear un punto de interés
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_punto_interes(punto: schemas.PuntoInteresCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    nuevo_punto = models.PuntoInteres(
        nombre=punto.nombre,
        tipo=punto.tipo,
        direccion=punto.direccion,
        latitud=punto.latitud,
        longitud=punto.longitud,
        usuario_id=current_user.id  # Asignar al usuario que lo crea
    )
    db.add(nuevo_punto)
    db.commit()
    db.refresh(nuevo_punto)
    return nuevo_punto

# Obtener todos los puntos de interés
@router.get("/")
def get_puntos_interes(db: Session = Depends(get_db)):
    return db.query(models.PuntoInteres).all()

# Obtener un punto de interés por ID
@router.get("/{punto_id}")
def get_punto_interes(punto_id: int, db: Session = Depends(get_db)):
    punto = db.query(models.PuntoInteres).filter(models.PuntoInteres.id == punto_id).first()
    if not punto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Punto de interés no encontrado")
    return punto

# Actualizar un punto de interés (solo creador o admin)
@router.put("/{punto_id}")
def update_punto_interes(punto_id: int, punto_update: schemas.PuntoInteresUpdate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    punto = db.query(models.PuntoInteres).filter(models.PuntoInteres.id == punto_id).first()
    if not punto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Punto de interés no encontrado")
    
    if punto.usuario_id != current_user.id and current_user.rol != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para modificar este punto de interés")
    
    for key, value in punto_update.dict(exclude_unset=True).items():
        setattr(punto, key, value)
    
    db.commit()
    db.refresh(punto)
    return punto

# Eliminar un punto de interés (solo creador o admin)
@router.delete("/{punto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_punto_interes(punto_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    punto = db.query(models.PuntoInteres).filter(models.PuntoInteres.id == punto_id).first()
    if not punto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Punto de interés no encontrado")
    
    if punto.usuario_id != current_user.id and current_user.rol != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para eliminar este punto de interés")
    
    db.delete(punto)
    db.commit()
    return {"message": "Punto de interés eliminado exitosamente"}
