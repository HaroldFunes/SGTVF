from fastapi import APIRouter, Query, HTTPException, Request
from models.estado_proyecto import EstadoProyecto
from controllers.estado_proyecto import (
    create_estado_proyecto,
    get_estados_proyecto,
    get_estado_proyecto_by_id,
    update_estado_proyecto,
    delete_estado_proyecto
)
from utils.security import validateadmin

router = APIRouter(prefix="/estados-proyecto", tags=["📊 Estados de Proyecto"])

@router.post("/", summary="Crear nuevo estado de proyecto", response_model=EstadoProyecto)
@validateadmin
async def create_new_estado_proyecto(
    request: Request,
    estado_proyecto_data: EstadoProyecto
):
    result = await create_estado_proyecto(estado_proyecto_data)
    return result

@router.get("/", summary="Obtener todos los estados de proyecto", response_model=list[EstadoProyecto])
@validateadmin
async def get_all_estados_proyecto(
    request: Request,
    skip: int = Query(default=0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(default=50, ge=1, le=100, description="Número de registros a obtener")
):
    result = await get_estados_proyecto()
    return result[skip : skip + limit]

@router.get("/{estado_proyecto_id}", summary="Obtener estado de proyecto por ID", response_model=EstadoProyecto)
@validateadmin
async def get_single_estado_proyecto(
    request: Request,
    estado_proyecto_id: str
):
    result = await get_estado_proyecto_by_id(estado_proyecto_id)
    return result

@router.put("/{estado_proyecto_id}", summary="Actualizar estado de proyecto", response_model=EstadoProyecto)
@validateadmin
async def update_single_estado_proyecto(
    request: Request,
    estado_proyecto_id: str,
    estado_proyecto_data: EstadoProyecto
):
    result = await update_estado_proyecto(estado_proyecto_id, estado_proyecto_data)
    return result

@router.delete("/{estado_proyecto_id}", summary="Eliminar estado de proyecto")
@validateadmin
async def delete_single_estado_proyecto(
    request: Request,
    estado_proyecto_id: str
):
    result = await delete_estado_proyecto(estado_proyecto_id)
    return result