from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from sqlalchemy.sql import func
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "inmobiliaria"}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # Se usa hashed_password en lugar de contrasena
    rol = Column(String, default="usuario", nullable=False)
    creado_en = Column(TIMESTAMP, server_default=func.now(), nullable=False)  # Genera la fecha automáticamente

    propiedades = relationship("Propiedad", back_populates="usuario") 
    puntos_interes = relationship("PuntoInteres", back_populates="usuario")

class Propiedad(Base):
    __tablename__ = "propiedades"
    __table_args__ = {"schema": "inmobiliaria"}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    superficie = Column(Float, nullable=True)
    habitaciones = Column(Integer, nullable=True)
    banos = Column(Integer, nullable=True)
    precio_estimado = Column(Float, nullable=True)
    geom = Column(Geometry("POINT", srid=4326))  # Se agrega SRID para evitar problemas en PostgreSQL
    usuario_id = Column(Integer, ForeignKey("inmobiliaria.usuarios.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="propiedades")  # Se enlaza correctamente con Usuario

class PuntoInteres(Base):
    __tablename__ = "puntos_interes"
    __table_args__ = {"schema": "inmobiliaria"}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    geom = Column(Geometry("POINT", srid=4326))
    usuario_id = Column(Integer, ForeignKey("inmobiliaria.usuarios.id"))  # 📌 Agregar clave foránea

    usuario = relationship("Usuario", back_populates="puntos_interes")  # Se agrega SRID para evitar errores
