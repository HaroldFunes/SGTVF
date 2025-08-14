from fastapi import APIRouter, Query, HTTPException, Request
from models.categoria_tarea import CategoriaTarea
from controllers.categoria_tarea import (
    create_categoria_tarea,
    get_categorias_tarea,
    get_categoria_tarea_by_id,
    update_categoria_tarea,
    delete_categoria_tarea
)
from utils.security import validateadmin

router = APIRouter(prefix="/categorias-tarea", tags=["🗂️ Categorias de Tarea"])

@router.post("/", summary="Crear nueva categoría de tarea", response_model=CategoriaTarea)
@validateadmin
async def create_new_categoria_tarea(
    request: Request,
    categoria_tarea_data: CategoriaTarea
):
    result = await create_categoria_tarea(categoria_tarea_data)
    return result

@router.get("/", summary="Obtener todas las categorías de tarea", response_model=list[CategoriaTarea])
@validateadmin
async def get_all_categorias_tarea(
    request: Request,
    skip: int = Query(default=0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(default=50, ge=1, le=100, description="Número de registros a obtener")
):
    result = await get_categorias_tarea()
    return result[skip : skip + limit]

@router.get("/{categoria_tarea_id}", summary="Obtener categoría de tarea por ID", response_model=CategoriaTarea)
@validateadmin
async def get_single_categoria_tarea(
    request: Request,
    categoria_tarea_id: str
):
    result = await get_categoria_tarea_by_id(categoria_tarea_id)
    return result

@router.put("/{categoria_tarea_id}", summary="Actualizar categoría de tarea", response_model=CategoriaTarea)
@validateadmin
async def update_single_categoria_tarea(
    request: Request,
    categoria_tarea_id: str,
    categoria_tarea_data: CategoriaTarea
):
    result = await update_categoria_tarea(categoria_tarea_id, categoria_tarea_data)
    return result

@router.delete("/{categoria_tarea_id}", summary="Eliminar categoría de tarea")
@validateadmin
async def delete_single_categoria_tarea(
    request: Request,
    categoria_tarea_id: str
):
    result = await delete_categoria_tarea(categoria_tarea_id)
    return result