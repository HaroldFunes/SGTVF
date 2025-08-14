from models.estado_tarea import EstadoTarea
from utils.mongodb import get_collection
from fastapi import HTTPException
from bson import ObjectId

coll = get_collection("estados_tarea")

async def create_estado_tarea(estado_tarea: EstadoTarea) -> EstadoTarea:
    try:
        estado_tarea.nombre_estado = estado_tarea.nombre_estado.strip().lower()

        existing_state = coll.find_one({"nombre_estado": estado_tarea.nombre_estado})
        if existing_state:
            raise HTTPException(status_code=400, detail="Task state with this name already exists")

        estado_tarea_dict = estado_tarea.model_dump(exclude={"id"})
        inserted = coll.insert_one(estado_tarea_dict)
        estado_tarea.id = str(inserted.inserted_id)
        return estado_tarea
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating task state: {str(e)}")

async def get_estados_tarea() -> list[EstadoTarea]:
    try:
        estados_tarea = []
        for doc in coll.find():
            doc['id'] = str(doc['_id'])
            del doc['_id']
            estados_tarea.append(EstadoTarea(**doc))
        return estados_tarea
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching task states: {str(e)}")

async def get_estado_tarea_by_id(estado_tarea_id: str) -> EstadoTarea:
    try:
        doc = coll.find_one({"_id": ObjectId(estado_tarea_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Task state not found")

        doc['id'] = str(doc['_id'])
        del doc['_id']
        return EstadoTarea(**doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching task state: {str(e)}")

async def update_estado_tarea(estado_tarea_id: str, estado_tarea: EstadoTarea) -> EstadoTarea:
    try:
        estado_tarea.nombre_estado = estado_tarea.nombre_estado.strip().lower()

        existing_state = coll.find_one({"nombre_estado": estado_tarea.nombre_estado, "_id": {"$ne": ObjectId(estado_tarea_id)}})
        if existing_state:
            raise HTTPException(status_code=400, detail="Task state with this name already exists")

        result = coll.update_one(
            {"_id": ObjectId(estado_tarea_id)},
            {"$set": estado_tarea.model_dump(exclude={"id"})}
        )
        if result.modified_count == 0:
            if coll.find_one({"_id": ObjectId(estado_tarea_id)}) is None:
                raise HTTPException(status_code=404, detail="Task state not found")
            return await get_estado_tarea_by_id(estado_tarea_id)
        
        return await get_estado_tarea_by_id(estado_tarea_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating task state: {str(e)}")

async def delete_estado_tarea(estado_tarea_id: str):
    try:
        result = coll.delete_one({"_id": ObjectId(estado_tarea_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Task state not found")
        return {"message": "Task state deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting task state: {str(e)}")