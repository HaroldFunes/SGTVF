from fastapi import APIRouter, Query, HTTPException, Request
from models.estado_tarea import EstadoTarea
from controllers.estado_tarea import (
    create_estado_tarea,
    get_estados_tarea,
    get_estado_tarea_by_id,
    update_estado_tarea,
    delete_estado_tarea
)
from utils.security import validateadmin

router = APIRouter(prefix="/estados-tarea", tags=["📝 Estados de Tarea"])

@router.post("/", summary="Crear nuevo estado de tarea", response_model=EstadoTarea)
@validateadmin
async def create_new_estado_tarea(
    request: Request,
    estado_tarea_data: EstadoTarea
):
    result = await create_estado_tarea(estado_tarea_data)
    return result

@router.get("/", summary="Obtener todos los estados de tarea", response_model=list[EstadoTarea])
@validateadmin
async def get_all_estados_tarea(
    request: Request,
    skip: int = Query(default=0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(default=50, ge=1, le=100, description="Número de registros a obtener")
):
    result = await get_estados_tarea()
    return result[skip : skip + limit]

@router.get("/{estado_tarea_id}", summary="Obtener estado de tarea por ID", response_model=EstadoTarea)
@validateadmin
async def get_single_estado_tarea(
    request: Request,
    estado_tarea_id: str
):
    result = await get_estado_tarea_by_id(estado_tarea_id)
    return result

@router.put("/{estado_tarea_id}", summary="Actualizar estado de tarea", response_model=EstadoTarea)
@validateadmin
async def update_single_estado_tarea(
    request: Request,
    estado_tarea_id: str,
    estado_tarea_data: EstadoTarea
):
    result = await update_estado_tarea(estado_tarea_id, estado_tarea_data)
    return result

@router.delete("/{estado_tarea_id}", summary="Eliminar estado de tarea")
@validateadmin
async def delete_single_estado_tarea(
    request: Request,
    estado_tarea_id: str
):
    result = await delete_estado_tarea(estado_tarea_id)
    return result