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
#@validateuser
async def create_new_proyecto(
    request: Request,
    proyecto_data: Proyecto
):
    """
    Crea un nuevo proyecto.
    Requiere autenticación de usuario.
    """
    result = await create_proyecto(proyecto_data)
    return result

@router.get("/", summary="Obtener proyectos", response_model=list[Proyecto])
#@validateuser
async def get_all_proyectos(
    request: Request,
    skip: int = Query(default=0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(default=50, ge=1, le=100, description="Número de registros a obtener")
):
    """
    Obtener proyectos:
    - Admin: todas los proyectos del sistema
    - Usuario: solo los proyectos a los que tiene acceso (si se implementa en controlador)
    """
    is_admin = getattr(request.state, 'admin', False)
    result = await get_proyectos()
    return result[skip : skip + limit]

@router.get("/{proyecto_id}", summary="Obtener proyecto por ID", response_model=Proyecto)
#@validateuser
async def get_single_proyecto(
    request: Request,
    proyecto_id: str
):
    """
    Obtener un proyecto específico por su ID.
    - Admin: cualquier proyecto
    - Usuario: solo si tiene acceso al proyecto (ej. es creador o asignado)
    """
    is_admin = getattr(request.state, 'admin', False)
    result = await get_proyecto_by_id(proyecto_id)
    return result

@router.put("/{proyecto_id}", summary="Actualizar proyecto", response_model=Proyecto)
#@validateuser
async def update_single_proyecto(
    request: Request,
    proyecto_id: str,
    proyecto_data: Proyecto
):
    """
    Actualiza un proyecto existente por su ID.
    Requiere autenticación de usuario. Los administradores pueden actualizar cualquier proyecto,
    los usuarios regulares solo los proyectos a los que tienen acceso (si se implementa lógica de acceso en controlador).
    """
    is_admin = getattr(request.state, 'admin', False)
    result = await update_proyecto(proyecto_id, proyecto_data)
    return result

@router.put("/{proyecto_id}/deactivate", summary="Desactivar proyecto", response_model=Proyecto)
#@validateadmin
async def deactivate_single_proyecto(
    request: Request,
    proyecto_id: str
):
    """
    Desactiva un proyecto por su ID.
    Requiere permisos de administrador.
    """
    result = await deactivate_proyecto(proyecto_id)
    return result