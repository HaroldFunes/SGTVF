import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from bson import ObjectId
from jose import jwt, JWTError

from database import get_database_client # Ajusta esta importación a tu archivo de conexión DB

from models.login import Login
from models.usuario import Usuario

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "tu_super_clave_secreta_aqui_CAMBIAR_EN_PRODUCCION")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea un JWT token con los datos proporcionados y tiempo de expiración."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def login(login_data: Login) -> dict:
    db_client = await get_database_client()
    usuarios_collection = db_client["your_database_name"]["usuarios"]

    user_document = await usuarios_collection.find_one({"email": login_data.email})

    if not user_document:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas: Correo o contraseña inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_db = Usuario(**user_document)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user_db.id), "email": user_db.email, "rol": user_db.rol},
        expires_delta=access_token_expires
    )

    return {
        "success": True,
        "message": "Login exitoso",
        "access_token": access_token,
        "token_type": "bearer"
    }

async def register_user(user_data: Usuario) -> dict:
    db_client = await get_database_client()
    usuarios_collection = db_client["your_database_name"]["usuarios"]

    user_dict = user_data.model_dump(by_alias=True, exclude_unset=True)
    if "_id" not in user_dict:
        user_dict["_id"] = ObjectId()
    if "password" in user_dict:
        user_dict["hashed_password"] = check_password_hash(user_dict["password"], "")
        del user_dict["password"]

    result = await usuarios_collection.insert_one(user_dict)
    
    return {
        "success": True,
        "message": "Usuario registrado exitosamente",
        "user_id": str(result.inserted_id)
    }