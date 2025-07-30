from models.rol import Rol  # Asumiendo que Rol está en models/rol.py
from utils.mongodb import get_collection
from fastapi import HTTPException
from bson import ObjectId

# Obtener la colección de MongoDB para roles
coll = get_collection("roles")

async def create_rol(rol: Rol) -> Rol:
    try:
        rol.nombre_rol = rol.nombre_rol.strip().lower()

        existing_rol = coll.find_one({"nombre_rol": rol.nombre_rol})
        if existing_rol:
            raise HTTPException(status_code=400, detail="Rol with this name already exists")

        # Excluir 'id' del diccionario para que MongoDB genere el _id
        rol_dict = rol.model_dump(exclude={"id"})
        inserted = coll.insert_one(rol_dict)
        rol.id = str(inserted.inserted_id) # Asignar el _id generado de vuelta al modelo Pydantic
        return rol
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating rol: {str(e)}")

async def get_roles() -> list[Rol]:
    try:
        roles = []
        for doc in coll.find():
            doc['id'] = str(doc['_id']) # Mapear _id a id para el modelo Pydantic
            del doc['_id']
            roles.append(Rol(**doc))
        return roles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching roles: {str(e)}")

async def get_rol_by_id(rol_id: str) -> Rol:
    try:
        # Usar ObjectId para buscar por _id en MongoDB
        doc = coll.find_one({"_id": ObjectId(rol_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Rol not found")

        doc['id'] = str(doc['_id'])
        del doc['_id']
        return Rol(**doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching rol: {str(e)}")

async def update_rol(rol_id: str, rol: Rol) -> Rol:
    try:
        rol.nombre_rol = rol.nombre_rol.strip().lower()

        # Verificar si ya existe otro rol con el mismo nombre (excluyendo el actual por su ID)
        existing_rol = coll.find_one({"nombre_rol": rol.nombre_rol, "_id": {"$ne": ObjectId(rol_id)}})
        if existing_rol:
            raise HTTPException(status_code=400, detail="Rol with this name already exists")

        # Excluir 'id' ya que no queremos actualizar el _id
        result = coll.update_one(
            {"_id": ObjectId(rol_id)},
            {"$set": rol.model_dump(exclude={"id"})}
        )
        if result.modified_count == 0:
            # Podría ser 0 si no se encontró el rol o si los datos no cambiaron
            # Aquí asumimos que si no se modificó, es porque no se encontró
            if coll.find_one({"_id": ObjectId(rol_id)}) is None:
                raise HTTPException(status_code=404, detail="Rol not found")
            # Si se encontró pero no se modificó, retornamos el rol existente
            return await get_rol_by_id(rol_id)
        
        return await get_rol_by_id(rol_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating rol: {str(e)}")

async def delete_rol(rol_id: str):
    try:
        result = coll.delete_one({"_id": ObjectId(rol_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Rol not found")
        return {"message": "Rol deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting rol: {str(e)}")