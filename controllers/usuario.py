import os
import json
import logging
from dotenv import load_dotenv
import requests
import base64
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from models.usuario import Usuario
from models.usuario_salida import UsuarioSalida
from utils.mongodb import get_collection
from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime
from models.login import Login
from utils.security import create_jwt_token
coll = get_collection("usuarios")

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_firebase():
    if firebase_admin._apps:
        return

    try:
        firebase_creds_base64 = os.getenv("FIREBASE_CREDENTIALS_BASE64")

        if firebase_creds_base64:
            firebase_creds_json = base64.b64decode(firebase_creds_base64).decode('utf-8')
            firebase_creds = json.loads(firebase_creds_json)
            cred = credentials.Certificate(firebase_creds)
            firebase_admin.initialize_app(cred)
            logger.info("Firebase initialized with environment variable credentials")
        else:
            cred = credentials.Certificate("secrets/SGTFirebase-secrets.json")
            firebase_admin.initialize_app(cred)
            logger.info("Firebase initialized with JSON file")

    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")
        raise HTTPException(status_code=500, detail=f"Firebase configuration error: {str(e)}")


initialize_firebase()

async def create_usuario(usuario: Usuario) -> Usuario:
    registro_usuario = {}
    try:
        registro_usuario = firebase_auth.create_user(
            email = usuario.email,
            password = usuario.password

        )
    except Exception as e:
        logger.warning( e )
        raise HTTPException(
            status_code=400,
            detail="Error al registrar usuario en firebase"
        )
    try:
        usuario.email = usuario.email.strip().lower()

        existing_user = coll.find_one({"email": usuario.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        usuario_dict = usuario.model_dump(exclude={"id","password"})
        usuario_dict["fecha_registro"] = usuario.fecha_registro
        
        inserted = coll.insert_one(usuario_dict)
        usuario.id = str(inserted.inserted_id)
        return usuario
    except Exception as e:
        firebase_auth.delete_user(registro_usuario.uid)

        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")
    
async def login(user: Login) -> dict:
    api_key = os.getenv("FIREBASE_API_KEY")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {
        "email": user.email
        , "password": user.password
        , "returnSecureToken": True
    }

    response = requests.post(url, json = payload)
    response_data = response.json()

    if "error" in response_data:
        raise HTTPException(
            status_code=400
            , detail="Error al autenticar usuario"
        )
    
    coll = get_collection("usuarios")
    user_info = coll.find_one({ "email": user.email })

    if not user_info:
        raise HTTPException(
            status_code=404
            , detail="Usuario no encontrado en la base de datos"
        )
    return {
        "message": "Usuario Autenticado correctamente"
        , "idToken": create_jwt_token(
            str(user_info["_id"]),
            user_info["email"],
            user_info["nombre"],
            user_info["rol"]
        )
    }


async def get_usuarios() -> list[UsuarioSalida]:
    try:
        usuarios = []
        for doc in coll.find():
            doc['id'] = str(doc['_id'])
            del doc['_id']
            usuarios.append(UsuarioSalida(**doc))
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

async def get_usuario_by_id(usuario_id: str) -> UsuarioSalida:
    try:
        doc = coll.find_one({"_id": ObjectId(usuario_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="User not found")

        doc['id'] = str(doc['_id'])
        del doc['_id']
        return UsuarioSalida(**doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

async def update_usuario(usuario_id: str, usuario: Usuario) -> Usuario:
    try:
        usuario.email = usuario.email.strip().lower()

        existing_user = coll.find_one({"email": usuario.email, "_id": {"$ne": ObjectId(usuario_id)}})
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")

        usuario_dict = usuario.model_dump(exclude={"id"})
        
        result = coll.update_one(
            {"_id": ObjectId(usuario_id)},
            {"$set": usuario_dict}
        )
        if result.modified_count == 0:
            if coll.find_one({"_id": ObjectId(usuario_id)}) is None:
                raise HTTPException(status_code=404, detail="User not found")
            return await get_usuario_by_id(usuario_id)
        
        return await get_usuario_by_id(usuario_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

async def delete_usuario(usuario_id: str):
    try:
        result = coll.delete_one({"_id": ObjectId(usuario_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")