from models.proyecto import Proyecto
from utils.mongodb import get_collection
from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime

coll = get_collection("proyectos")

async def create_proyecto(proyecto: Proyecto) -> Proyecto:
    try:
        proyecto.nombre_proyecto = proyecto.nombre_proyecto.strip()

        existing_project = coll.find_one({"nombre_proyecto": proyecto.nombre_proyecto})
        if existing_project:
            raise HTTPException(status_code=400, detail="Project with this name already exists")
        
        proyecto_dict = proyecto.model_dump(exclude={"id"})
        proyecto_dict["fecha_creacion"] = proyecto.fecha_creacion
        proyecto_dict["fecha_actualizacion"] = proyecto.fecha_actualizacion
        
        inserted = coll.insert_one(proyecto_dict)
        proyecto.id = str(inserted.inserted_id)
        return proyecto
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating project: {str(e)}")

async def get_proyectos() -> list[Proyecto]:
    try:
        proyectos = []
        for doc in coll.find():
            doc['id'] = str(doc['_id'])
            del doc['_id']
            proyectos.append(Proyecto(**doc))
        return proyectos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching projects: {str(e)}")

async def get_proyecto_by_id(proyecto_id: str) -> Proyecto:
    try:
        doc = coll.find_one({"_id": ObjectId(proyecto_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Project not found")

        doc['id'] = str(doc['_id'])
        del doc['_id']
        return Proyecto(**doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching project: {str(e)}")

async def update_proyecto(proyecto_id: str, proyecto: Proyecto) -> Proyecto:
    try:
        proyecto.nombre_proyecto = proyecto.nombre_proyecto.strip()

        existing_project = coll.find_one({"nombre_proyecto": proyecto.nombre_proyecto, "_id": {"$ne": ObjectId(proyecto_id)}})
        if existing_project:
            raise HTTPException(status_code=400, detail="Project with this name already exists")

        proyecto_dict = proyecto.model_dump(exclude={"id"})
        proyecto_dict["fecha_actualizacion"] = datetime.now()
        
        result = coll.update_one(
            {"_id": ObjectId(proyecto_id)},
            {"$set": proyecto_dict}
        )
        if result.modified_count == 0:
            if coll.find_one({"_id": ObjectId(proyecto_id)}) is None:
                raise HTTPException(status_code=404, detail="Project not found")
            return await get_proyecto_by_id(proyecto_id)
        
        return await get_proyecto_by_id(proyecto_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating project: {str(e)}")

async def deactivate_proyecto(proyecto_id: str) -> Proyecto:
    try:
        result = coll.update_one(
            {"_id": ObjectId(proyecto_id)},
            {"$set": {"estado": "desactivado"}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Project not found")

        return await get_proyecto_by_id(proyecto_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deactivating project: {str(e)}")