from fastapi import FastAPI
from .database import engine
from .models import Base

from app.routers import auth, propiedades, puntos_interes

app = FastAPI(
    title="API de Inmuebles",
    description="API para gestión de propiedades y autenticación",
    version="1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
app.include_router(propiedades.router, prefix="/propiedades", tags=["Propiedades"])
app.include_router(puntos_interes.router, prefix="/puntos-interes", tags=["Puntos de Interés"])