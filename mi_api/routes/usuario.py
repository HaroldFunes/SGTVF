from fastapi import APIRouter, Query, HTTPException, Request
from models.usuario import Usuario
from models.usuario_salida import UsuarioSalida
from controllers.usuario import (
    create_usuario,
    get_usuarios,
    get_usuario_by_id,
    update_usuario,
    delete_usuario
)
from utils.security import validateuser, validateadmin

router = APIRouter(prefix="/usuarios", tags=["👤 Usuarios"])

@router.post("/", summary="Crear nuevo usuario", response_model=Usuario)
@validateadmin
async def create_new_usuario(
    request: Request,
    usuario_data: Usuario
):
    result = await create_usuario(usuario_data)
    return result

@router.get("/", summary="Obtener usuarios", response_model=list[UsuarioSalida])
@validateadmin
async def get_all_usuarios(
    request: Request,
    skip: int = Query(default=0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(default=50, ge=1, le=100, description="Número de registros a obtener")
):
    result = await get_usuarios()
    return result[skip : skip + limit]

@router.get("/{usuario_id}", summary="Obtener usuario por ID", response_model=UsuarioSalida)
@validateuser
async def get_single_usuario(
    request: Request,
    usuario_id: str
):
    is_admin = getattr(request.state, 'admin', False)
    requesting_user_id = request.state.id

    if not is_admin and usuario_id != requesting_user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este usuario.")
        
    result = await get_usuario_by_id(usuario_id)
    return result

@router.put("/{usuario_id}", summary="Actualizar usuario", response_model=Usuario)
@validateuser
async def update_single_usuario(
    request: Request,
    usuario_id: str,
    usuario_data: Usuario
):
    is_admin = getattr(request.state, 'admin', False)
    requesting_user_id = request.state.id

    if not is_admin and usuario_id != requesting_user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar este usuario.")

    if not is_admin:
        current_user = await get_usuario_by_id(usuario_id)
        if usuario_data.rol != current_user.rol:
            raise HTTPException(status_code=403, detail="No tienes permiso para cambiar tu rol.")
        if usuario_data.firebase_uid != current_user.firebase_uid:
            raise HTTPException(status_code=403, detail="No tienes permiso para cambiar tu Firebase UID.")

    result = await update_usuario(usuario_id, usuario_data)
    return result

@router.delete("/{usuario_id}", summary="Eliminar usuario")
@validateadmin
async def delete_single_usuario(
    request: Request,
    usuario_id: str
):
    result = await delete_usuario(usuario_id)
    return result