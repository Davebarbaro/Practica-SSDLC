from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, func
from typing import Optional
import math
from app.models.vulnerability import Vulnerability
from app.core.database import get_session
from app.models.vuln_schemas import Severity, VulnerabilitiesListResponse


# Creamos un router para manejar rutas de vulnerabilidades

router = APIRouter()


# Ruta para listar vulnerabilidades que tiene separación por páginas y filtrado por severidad
#
@router.get("/", response_model=VulnerabilitiesListResponse)
async def list_vulnerabilities(
    page: int = Query(1, ge=1),                       # Página solicitada, mínimo 1
    limit: int = Query(10, ge=1, le=100),            # Cantidad de resultados por página, entre 1 y 100
    severity: Optional[Severity] = None,             # Filtrar por severidad opcional
    session: Session = Depends(get_session)          # Sesión de base de datos
):
   
    # Consulta base: vulnerabilidades activas
    statement = select(Vulnerability).where(Vulnerability.status == "active") # Consulta base

   # Filtrado por severidad si se proporcionó
    if severity:
        statement = statement.where(Vulnerability.severity == severity.value)

    # Contar el total de resultados para la paginación

    count_statement = select(func.count()).select_from(Vulnerability).where(
        Vulnerability.status == "active"
    )

    if severity: # Si se proporcionó un filtro de severidad entonces añadimos esa condición a la consulta que cuenta el total de vulnerabilidades
        count_statement = count_statement.where(
            Vulnerability.severity == severity.value
        )

    total = session.exec(count_statement).one()  # Total de vulnerabilidades que cumplen el filtro

    
    # Obtener los resultados de la página solicitada
    
    results = session.exec(
        statement.offset((page - 1) * limit).limit(limit)
    ).all()  # Aplicamos ofset (paginación) y limmit (número de resultados por página)

    # Calcular total de páginas
    total_pages = math.ceil(total / limit) if total > 0 else 1 # Si no hay resultados, al menos una página vacía

   
    # Devolver la respuesta con resultados y metadatos de paginación
   
    return {
        "vulnerabilities": results,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages
    }