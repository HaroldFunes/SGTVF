import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from bson import ObjectId
from jose import jwt, JWTError

# Asumo que tu cliente de DB se obtiene así. Ajusta según tu implementación.
from database import get_database_client # Ajusta esta importación a tu archivo de conexión DB

# Asumo que el modelo Login está en models/login.py
from models.login import Login
# Asumo que el modelo Usuario está en models/usuario.py
from models.usuario import Usuario

# --- Configuración JWT ---
# Es CRÍTICO que esta clave se cargue desde variables de entorno y NO esté hardcodeada.
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "tu_super_clave_secreta_aqui_CAMBIAR_EN_PRODUCCION")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # El token expirará en 30 minutos

# --- Funciones de Utilidad (placeholders) ---
# Necesitas implementar la verificación de hash de contraseña real.
# Por ejemplo, si usas bcrypt: `import bcrypt; bcrypt.checkpw(password.encode('utf-8'), hashed_password)`
def check_password_hash(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si la contraseña plana coincide con el hash.
    ESTO ES UN PLACEHOLDER. Reemplazar con una librería de hashing real (ej. bcrypt).
    """
    # Ejemplo con bcrypt (necesitarías instalarlo: pip install bcrypt)
    # import bcrypt
    # return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    # Para propósitos de demostración, una comprobación simple (NO USAR EN PRODUCCIÓN)
    # return plain_password == hashed_password # Peligroso si no está hasheado
    
    # Si las contraseñas en tu DB no están hasheadas y son texto plano (MALO, PERO PARA PRUEBA INICIAL)
    return plain_password == hashed_password 
    
    # En un escenario real, asumes que el `hashed_password` ya es un byte string
    # o lo codificas antes de pasarlo a `checkpw`.
    # return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)


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

# --- Lógica del Controlador de Autenticación ---

async def login(login_data: Login) -> dict:
    """
    Función de login para autenticar un usuario.
    Verifica las credenciales y genera un token JWT.
    """
    db_client = await get_database_client()
    usuarios_collection = db_client["your_database_name"]["usuarios"] # Ajusta "your_database_name" y "usuarios"

    # Buscar usuario por email
    user_document = await usuarios_collection.find_one({"email": login_data.email})

    if not user_document:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas: Correo o contraseña inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convertir el documento a un modelo Usuario para fácil acceso a los campos
    user_db = Usuario(**user_document)
    
    # Verificar contraseña hasheada
    # Asegúrate de que user_db.hashed_password existe y es el hash de la contraseña
    if not check_password_hash(login_data.password, user_db.hashed_password): # Asumo campo 'hashed_password' en tu modelo/DB
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas: Correo o contraseña inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generar token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user_db.id), "email": user_db.email, "rol": user_db.rol}, # Guardar id de mongo, email y rol
        expires_delta=access_token_expires
    )

    return {
        "success": True,
        "message": "Login exitoso",
        "access_token": access_token,
        "token_type": "bearer"
    }

# Si necesitas una función para el registro, podría ir aquí también.
async def register_user(user_data: Usuario) -> dict:
    """
    Función para registrar un nuevo usuario.
    Debería hashear la contraseña antes de guardarla.
    """
    db_client = await get_database_client()
    usuarios_collection = db_client["your_database_name"]["usuarios"]

    # Verificar si el usuario ya existe
    if await usuarios_collection.find_one({"email": user_data.email}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya está registrado.")

    # Hashear la contraseña (PLACEHOLDER)
    # import bcrypt
    # hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
    # user_data.hashed_password = hashed_password.decode('utf-8') # Guardar como string
    
    # Si 'password' es parte de tu Pydantic model de Usuario de entrada, deberías hashearlo aquí
    # y luego, opcionalmente, eliminar el campo de la respuesta o usar un modelo diferente para la salida.
    # Por ahora, asumo que `hashed_password` es un campo separado en la DB, no en el input `Usuario`.
    # Si `Usuario` ya tiene `hashed_password` al crearlo, asegúrate de que venga hasheado.

    user_dict = user_data.model_dump(by_alias=True, exclude_unset=True)
    # Asegúrate de que el ID sea ObjectId al insertar si no lo es ya
    if "_id" not in user_dict:
        user_dict["_id"] = ObjectId()
    # No queremos guardar la contraseña plana si la Pydantic la recibió
    if "password" in user_dict:
        # Aquí iría el hasheo de user_dict["password"]
        user_dict["hashed_password"] = check_password_hash(user_dict["password"], "") # Esto es un mal placeholder
        del user_dict["password"]

    # Insertar en la base de datos
    result = await usuarios_collection.insert_one(user_dict)
    
    return {
        "success": True,
        "message": "Usuario registrado exitosamente",
        "user_id": str(result.inserted_id)
    }