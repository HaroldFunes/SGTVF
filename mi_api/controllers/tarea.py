from models.tarea import Tarea
from utils.mongodb import get_collection
from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime

coll = get_collection("tareas")

async def create_tarea(tarea: Tarea) -> Tarea:
    try:
        tarea.actividad = tarea.actividad.strip()

        tarea_dict = tarea.model_dump(exclude={"id"})
        tarea_dict["fecha_creacion"] = tarea.fecha_creacion
        tarea_dict["fecha_actualizacion"] = tarea.fecha_actualizacion
        if tarea.fecha_fin:
            tarea_dict["fecha_fin"] = tarea.fecha_fin
        
        inserted = coll.insert_one(tarea_dict)
        tarea.id = str(inserted.inserted_id)
        return tarea
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")

async def get_tareas() -> list[Tarea]:
    try:
        tareas = []
        for doc in coll.find():
            doc['id'] = str(doc['_id'])
            del doc['_id']
            tareas.append(Tarea(**doc))
        return tareas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tasks: {str(e)}")

async def get_tarea_by_id(tarea_id: str) -> Tarea:
    try:
        doc = coll.find_one({"_id": ObjectId(tarea_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Tarea not found")

        doc['id'] = str(doc['_id'])
        del doc['_id']
        return Tarea(**doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tarea: {str(e)}")

async def update_tarea(tarea_id: str, tarea: Tarea) -> Tarea:
    try:
        tarea.actividad = tarea.actividad.strip()
        tarea_dict = tarea.model_dump(exclude={"id"})
        tarea_dict["fecha_actualizacion"] = datetime.now()
        if tarea.fecha_fin is None:
            coll.update_one({"_id": ObjectId(tarea_id)}, {"$unset": {"fecha_fin": ""}})
            del tarea_dict["fecha_fin"]
        elif "fecha_fin" in tarea_dict and tarea_dict["fecha_fin"] is not None:
             tarea_dict["fecha_fin"] = tarea.fecha_fin

        result = coll.update_one(
            {"_id": ObjectId(tarea_id)},
            {"$set": tarea_dict}
        )
        if result.modified_count == 0:
            if coll.find_one({"_id": ObjectId(tarea_id)}) is None:
                raise HTTPException(status_code=404, detail="Tarea not found")
            return await get_tarea_by_id(tarea_id)
        
        return await get_tarea_by_id(tarea_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating tarea: {str(e)}")

async def deactivate_tarea(tarea_id: str) -> Tarea:
    try:
        result = coll.update_one(
            {"_id": ObjectId(tarea_id)},
            {"$set": {"estado_tarea": "desactivada"}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Tarea not found")

        return await get_tarea_by_id(tarea_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deactivating task: {str(e)}")