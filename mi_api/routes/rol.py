from fastapi import APIRouter, Query, HTTPException, Request
from models.rol import Rol
from controllers.rol import (
    create_rol,
    get_roles,
    get_rol_by_id,
    update_rol,
    delete_rol
)
from utils.security import validateadmin

router = APIRouter(prefix="/roles", tags=["👤 Roles"])

@router.post("/", summary="Crear nuevo rol", response_model=Rol)
@validateadmin
async def create_new_rol(
    request: Request,
    rol_data: Rol
):
    result = await create_rol(rol_data)
    return result

@router.get("/", summary="Obtener todos los roles", response_model=list[Rol])
@validateadmin
async def get_all_roles(
    request: Request,
    skip: int = Query(default=0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(default=50, ge=1, le=100, description="Número de registros a obtener")
):
    result = await get_roles()
    return result[skip : skip + limit]

@router.get("/{rol_id}", summary="Obtener rol por ID", response_model=Rol)
@validateadmin
async def get_single_rol(
    request: Request,
    rol_id: str
):
    result = await get_rol_by_id(rol_id)
    return result

@router.put("/{rol_id}", summary="Actualizar rol", response_model=Rol)
@validateadmin
async def update_single_rol(
    request: Request,
    rol_id: str,
    rol_data: Rol
):
    result = await update_rol(rol_id, rol_data)
    return result

@router.delete("/{rol_id}", summary="Eliminar rol")
@validateadmin
async def delete_single_rol(
    request: Request,
    rol_id: str
):
    result = await delete_rol(rol_id)
    return result