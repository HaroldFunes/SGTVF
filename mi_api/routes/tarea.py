from fastapi import APIRouter, Query, HTTPException, Request
from models.tarea import Tarea
from controllers.tarea import (
    create_tarea,
    get_tareas,
    get_tarea_by_id,
    update_tarea,
    deactivate_tarea
)
from utils.security import validateuser, validateadmin

router = APIRouter(prefix="/tareas", tags=["✅ Tareas"])

@router.post("/", summary="Crear nueva tarea", response_model=Tarea)
@validateuser
async def create_new_tarea(
    request: Request,
    tarea_data: Tarea
):
    result = await create_tarea(tarea_data)
    return result

@router.get("/", summary="Obtener tareas", response_model=list[Tarea])
@validateuser
async def get_all_tareas(
    request: Request,
    skip: int = Query(default=0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(default=50, ge=1, le=100, description="Número de registros a obtener")
):
    is_admin = getattr(request.state, 'admin', False)
    result = await get_tareas()
    return result[skip : skip + limit]

@router.get("/{tarea_id}", summary="Obtener tarea por ID", response_model=Tarea)
@validateuser
async def get_single_tarea(
    request: Request,
    tarea_id: str
):
    is_admin = getattr(request.state, 'admin', False)
    result = await get_tarea_by_id(tarea_id)
    return result

@router.put("/{tarea_id}", summary="Actualizar tarea", response_model=Tarea)
@validateuser
async def update_single_tarea(
    request: Request,
    tarea_id: str,
    tarea_data: Tarea
):
    is_admin = getattr(request.state, 'admin', False)
    result = await update_tarea(tarea_id, tarea_data)
    return result

@router.put("/{tarea_id}/deactivate", summary="Desactivar tarea", response_model=Tarea)
@validateadmin
async def deactivate_single_tarea(
    request: Request,
    tarea_id: str
):
    result = await deactivate_tarea(tarea_id)
    return result