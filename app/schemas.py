from pydantic import BaseModel
from typing import Optional

"""Esquemas de Propiedades"""
class PropiedadCreate(BaseModel):
    nombre: str
    direccion: str
    latitud: float
    longitud: float
    superficie: Optional[float] = None
    habitaciones: Optional[int] = None
    banos: Optional[int] = None
    precio_estimado: Optional[float] = None
    geom: Optional[str] = None

class PropiedadUpdate(BaseModel):
    nombre: Optional[str]
    direccion: Optional[str]
    latitud: Optional[float]
    longitud: Optional[float]
    superficie: Optional[float]
    habitaciones: Optional[int]
    banos: Optional[int]
    precio_estimado: Optional[float]

"""Esquemas de Puntos de interes"""
class PuntoInteresBase(BaseModel):
    nombre: str
    tipo: str
    direccion: str
    latitud: float
    longitud: float

class PuntoInteresCreate(PuntoInteresBase):
    """Esquema para crear un punto de interés."""
    pass

class PuntoInteresUpdate(BaseModel):
    """Esquema para actualizar un punto de interés (campos opcionales)."""
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    direccion: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None

class PuntoInteresResponse(PuntoInteresBase):
    """Esquema de respuesta con ID."""
    id: int

    class Config:
        from_attributes = True
