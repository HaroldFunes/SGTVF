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
    """
    Crea una nueva categoría para tareas.
    Requiere permisos de administrador.
    """
    result = await create_categoria_tarea(categoria_tarea_data)
    return result

@router.get("/", summary="Obtener todas las categorías de tarea", response_model=list[CategoriaTarea])
@validateadmin
async def get_all_categorias_tarea(
    request: Request,
    skip: int = Query(default=0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(default=50, ge=1, le=100, description="Número de registros a obtener")
):
    """
    Obtiene una lista de todas las categorías de tarea.
    Requiere permisos de administrador.
    """
    result = await get_categorias_tarea()
    # Asumiendo que el controlador get_categorias_tarea ya devuelve una lista completa
    return result[skip : skip + limit]

@router.get("/{categoria_tarea_id}", summary="Obtener categoría de tarea por ID", response_model=CategoriaTarea)
@validateadmin
async def get_single_categoria_tarea(
    request: Request,
    categoria_tarea_id: str
):
    """
    Obtiene los detalles de una categoría de tarea específica por su ID.
    Requiere permisos de administrador.
    """
    result = await get_categoria_tarea_by_id(categoria_tarea_id)
    return result

@router.put("/{categoria_tarea_id}", summary="Actualizar categoría de tarea", response_model=CategoriaTarea)
@validateadmin
async def update_single_categoria_tarea(
    request: Request,
    categoria_tarea_id: str,
    categoria_tarea_data: CategoriaTarea
):
    """
    Actualiza una categoría de tarea existente por su ID.
    Requiere permisos de administrador.
    """
    result = await update_categoria_tarea(categoria_tarea_id, categoria_tarea_data)
    return result

@router.delete("/{categoria_tarea_id}", summary="Eliminar categoría de tarea")
@validateadmin
async def delete_single_categoria_tarea(
    request: Request,
    categoria_tarea_id: str
):
    """
    Elimina una categoría de tarea por su ID.
    Requiere permisos de administrador.
    """
    result = await delete_categoria_tarea(categoria_tarea_id)
    return result