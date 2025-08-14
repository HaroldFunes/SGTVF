from fastapi import APIRouter, Query, HTTPException, Request
from models.proyecto import Proyecto
from controllers.proyecto import (
    create_proyecto,
    get_proyectos,
    get_proyecto_by_id,
    update_proyecto,
    deactivate_proyecto
)
from utils.security import validateuser, validateadmin

router = APIRouter(prefix="/proyectos", tags=["🚧 Proyectos"])

@router.post("/", summary="Crear nuevo proyecto", response_model=Proyecto)
@validateuser
async def create_new_proyecto(
    request: Request,
    proyecto_data: Proyecto
):
    result = await create_proyecto(proyecto_data)
    return result

@router.get("/", summary="Obtener proyectos", response_model=list[Proyecto])
@validateuser
async def get_all_proyectos(
    request: Request,
    skip: int = Query(default=0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(default=50, ge=1, le=100, description="Número de registros a obtener")
):
    is_admin = getattr(request.state, 'admin', False)
    result = await get_proyectos()
    return result[skip : skip + limit]

@router.get("/{proyecto_id}", summary="Obtener proyecto por ID", response_model=Proyecto)
@validateuser
async def get_single_proyecto(
    request: Request,
    proyecto_id: str
):
    is_admin = getattr(request.state, 'admin', False)
    result = await get_proyecto_by_id(proyecto_id)
    return result

@router.put("/{proyecto_id}", summary="Actualizar proyecto", response_model=Proyecto)
@validateuser
async def update_single_proyecto(
    request: Request,
    proyecto_id: str,
    proyecto_data: Proyecto
):
    is_admin = getattr(request.state, 'admin', False)
    result = await update_proyecto(proyecto_id, proyecto_data)
    return result

@router.put("/{proyecto_id}/deactivate", summary="Desactivar proyecto", response_model=Proyecto)
@validateadmin
async def deactivate_single_proyecto(
    request: Request,
    proyecto_id: str
):
    result = await deactivate_proyecto(proyecto_id)
    return result