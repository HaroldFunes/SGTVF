import os
from typing import Optional
import jwt  
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from jwt import PyJWTError 
from functools import wraps

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
security = HTTPBearer()

def create_jwt_token(
    user_id: str,
    email: str,
    nombre: str,       
    rol: str,          
    
    expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expiration = datetime.utcnow() + expires_delta
    else:
        expiration = datetime.utcnow() + timedelta(hours=1)
    
    token_payload = {
        "id": user_id,
        "email": email,
        "nombre": nombre,  
        "rol": rol,
        "exp": expiration,
        "iat": datetime.utcnow()
    }
    
    encoded_jwt = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def validateuser(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get('request')
        if not request:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request object not found in decorator.")

        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing.")

        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme. Must be Bearer.")
        except ValueError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header format.")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            user_id = payload.get("id")
            email = payload.get("email")
            nombre = payload.get("nombre") 
            rol = payload.get("rol")
            exp = payload.get("exp")

            if user_id is None or email is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token payload invalid: Missing user ID or email.")

            if datetime.utcfromtimestamp(exp) < datetime.utcnow():
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token.")

            if not rol:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user.")
            
            request.state.id = user_id
            request.state.email = email
            request.state.nombre = nombre
            request.state.rol = rol
            request.state.admin = (rol == "admin")

        except PyJWTError as e: 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token or expired token: {e}")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server error during token validation: {e}")

        return await func(*args, **kwargs)
    return wrapper

def validateadmin(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get('request')
        if not request:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request object not found in decorator.")

        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing.")

        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme. Must be Bearer.")
        except ValueError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header format.")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            user_id = payload.get("id")
            email = payload.get("email")
            nombre = payload.get("nombre")
            rol = payload.get("rol")
            exp = payload.get("exp")

            if user_id is None or email is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token payload invalid: Missing user ID or email.")

            if datetime.utcfromtimestamp(exp) < datetime.utcnow():
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token.")

            if rol != "admin":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not an administrator.")
            
            request.state.id = user_id
            request.state.email = email
            request.state.nombre = nombre
            request.state.rol = rol
            request.state.admin = True

        except PyJWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token or expired token: {e}")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server error during admin token validation: {e}")

        return await func(*args, **kwargs)
    return wrapper

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        user_id = payload.get("id")
        email = payload.get("email")
        nombre = payload.get("nombre")
        rol = payload.get("rol")
        exp = payload.get("exp")

        if user_id is None or email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Invalid: Missing user info.")
        
        if datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token.")
        
        return {
            "id": user_id,
            "email": email,
            "nombre": nombre,
            "rol": rol,
            "admin": (rol == "admin")
        }
            
    except PyJWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server error during token dependency validation: {e}")


async def get_current_admin_user(current_user: dict = Depends(get_current_user)) -> dict:
    if not current_user.get("admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not an administrator.")
    return current_user