from models.estado_proyecto import EstadoProyecto
from utils.mongodb import get_collection
from fastapi import HTTPException
from bson import ObjectId

coll = get_collection("estados_proyecto")

async def create_estado_proyecto(estado_proyecto: EstadoProyecto) -> EstadoProyecto:
    try:
        estado_proyecto.nombre_estado = estado_proyecto.nombre_estado.strip().lower()

        existing_state = coll.find_one({"nombre_estado": estado_proyecto.nombre_estado})
        if existing_state:
            raise HTTPException(status_code=400, detail="Project state with this name already exists")

        estado_proyecto_dict = estado_proyecto.model_dump(exclude={"id"})
        inserted = coll.insert_one(estado_proyecto_dict)
        estado_proyecto.id = str(inserted.inserted_id)
        return estado_proyecto
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating project state: {str(e)}")

async def get_estados_proyecto() -> list[EstadoProyecto]:
    try:
        estados_proyecto = []
        for doc in coll.find():
            doc['id'] = str(doc['_id'])
            del doc['_id']
            estados_proyecto.append(EstadoProyecto(**doc))
        return estados_proyecto
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching project states: {str(e)}")

async def get_estado_proyecto_by_id(estado_proyecto_id: str) -> EstadoProyecto:
    try:
        doc = coll.find_one({"_id": ObjectId(estado_proyecto_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Project state not found")

        doc['id'] = str(doc['_id'])
        del doc['_id']
        return EstadoProyecto(**doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching project state: {str(e)}")

async def update_estado_proyecto(estado_proyecto_id: str, estado_proyecto: EstadoProyecto) -> EstadoProyecto:
    try:
        estado_proyecto.nombre_estado = estado_proyecto.nombre_estado.strip().lower()

        existing_state = coll.find_one({"nombre_estado": estado_proyecto.nombre_estado, "_id": {"$ne": ObjectId(estado_proyecto_id)}})
        if existing_state:
            raise HTTPException(status_code=400, detail="Project state with this name already exists")

        result = coll.update_one(
            {"_id": ObjectId(estado_proyecto_id)},
            {"$set": estado_proyecto.model_dump(exclude={"id"})}
        )
        if result.modified_count == 0:
            if coll.find_one({"_id": ObjectId(estado_proyecto_id)}) is None:
                raise HTTPException(status_code=404, detail="Project state not found")
            return await get_estado_proyecto_by_id(estado_proyecto_id)
        
        return await get_estado_proyecto_by_id(estado_proyecto_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating project state: {str(e)}")

async def delete_estado_proyecto(estado_proyecto_id: str):
    try:
        result = coll.delete_one({"_id": ObjectId(estado_proyecto_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Project state not found")
        return {"message": "Project state deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting project state: {str(e)}")