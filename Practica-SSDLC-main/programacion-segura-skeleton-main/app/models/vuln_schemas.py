from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


# Definimos niveles de severidad de una vulnerabilidad
class Severity(str, Enum):
    LOW = "low"        
    MEDIUM = "medium"   
    HIGH = "high"       
    CRITICAL = "critical" 


# Modelo base de vulnerabilidad

class VulnerabilityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)          # Nombre de la vulnerabilidad
    description: str = Field(..., min_length=10, max_length=500)  # Descripción detallada, el field dice que es obligatotrio con ...
    severity: Severity                                           # Nivel de severidad (enum)


# Modelo para crear vulnerabilidad

class VulnerabilityCreate(VulnerabilityBase):
    pass  # Aqui heredamos todos los campos de VulnerabilityBase, el pass indica que no añadimos nada más


# Modelo para responder con una vulnerabilidad existente

class VulnerabilityResponse(VulnerabilityBase):
    id: int               # ID de la vulnerabilidad en la DB
    created_by: int       # ID del usuario que la creo
    created_at: datetime  # Fecha de creación
    status: str           # Estado de la vulnerabilidad (ej: abierta, cerrada)

    class Config:
        from_attributes = True  # Permite crear este modelo desde objetos ORM, es decir desde la base de datos


# Modelo para listar vulnerabilidades con paginación

class VulnerabilitiesListResponse(BaseModel):
    vulnerabilities: List[VulnerabilityResponse]  # Lista de vulnerabilidades
    total: int          # Total de vulnerabilidades encontradas
    page: int           # Página actual
    limit: int          # Cantidad de elementos por página
    total_pages: int    # Número total de páginas
