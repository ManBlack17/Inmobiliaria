from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.utils import get_current_user
from sqlalchemy.sql import text

router = APIRouter(tags=["Propiedades"])

# Crear una propiedad
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_propiedad(propiedad: schemas.PropiedadCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):

     # ✅ Generar la geometría correctamente en SQLAlchemy usando ST_GeomFromText
    geom = text(f"ST_GeomFromText('POINT({propiedad.longitud} {propiedad.latitud})', 4326)")

    nueva_propiedad = models.Propiedad(
        nombre=propiedad.nombre,
        direccion=propiedad.direccion,
        latitud=propiedad.latitud,
        longitud=propiedad.longitud,
        superficie=propiedad.superficie,
        habitaciones=propiedad.habitaciones,
        banos=propiedad.banos,
        precio_estimado=propiedad.precio_estimado,
        geom=geom,
        usuario_id=current_user.id
    )
    db.add(nueva_propiedad)
    db.commit()
    db.refresh(nueva_propiedad)
    return nueva_propiedad

# Obtener todas las propiedades
@router.get("/")
def get_propiedades(db: Session = Depends(get_db)):
    return db.query(models.Propiedad).all()

# Obtener una propiedad por ID
@router.get("/{propiedad_id}")
def get_propiedad(propiedad_id: int, db: Session = Depends(get_db)):
    propiedad = db.query(models.Propiedad).filter(models.Propiedad.id == propiedad_id).first()
    if not propiedad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Propiedad no encontrada")
    return propiedad

# Actualizar una propiedad (solo creador o admin)
@router.put("/{propiedad_id}")
def update_propiedad(propiedad_id: int, propiedad_update: schemas.PropiedadUpdate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    propiedad = db.query(models.Propiedad).filter(models.Propiedad.id == propiedad_id).first()
    if not propiedad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Propiedad no encontrada")
    
    if propiedad.usuario_id != current_user.id and current_user.rol != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para modificar esta propiedad")
    
    for key, value in propiedad_update.dict(exclude_unset=True).items():
        setattr(propiedad, key, value)
    
    db.commit()
    db.refresh(propiedad)
    return propiedad

# Eliminar una propiedad (solo creador o admin)
@router.delete("/{propiedad_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_propiedad(propiedad_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    propiedad = db.query(models.Propiedad).filter(models.Propiedad.id == propiedad_id).first()
    if not propiedad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Propiedad no encontrada")
    
    if propiedad.usuario_id != current_user.id and current_user.rol != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para eliminar esta propiedad")
    
    db.delete(propiedad)
    db.commit()
    return {"message": "Propiedad eliminada exitosamente"}