from models.tarea import Tarea
from utils.mongodb import get_collection
from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime

coll = get_collection("tareas")

async def create_tarea(tarea: Tarea) -> Tarea:
    try:
        tarea.actividad = tarea.actividad.strip()

        # Opcional: Podrías añadir validación para las FKs si necesitas que existan en sus colecciones
        # Por ejemplo, verificar si id_proyecto existe en la colección "proyectos"
        
        tarea_dict = tarea.model_dump(exclude={"id"})
        # Asegurarse que las fechas se guarden correctamente
        tarea_dict["fecha_creacion"] = tarea.fecha_creacion
        tarea_dict["fecha_actualizacion"] = tarea.fecha_actualizacion
        if tarea.fecha_fin:
            tarea_dict["fecha_fin"] = tarea.fecha_fin # Si es Optional, solo se añade si existe
        
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

        # Opcional: Re-validar las FKs si es necesario

        tarea_dict = tarea.model_dump(exclude={"id"})
        # Siempre actualizar la fecha_actualizacion al modificar
        tarea_dict["fecha_actualizacion"] = datetime.now()
        # Asegurarse de manejar fecha_fin correctamente si es None
        if tarea.fecha_fin is None:
            # Eliminar el campo si se envía como None y ya existe en BD para limpiarlo
            coll.update_one({"_id": ObjectId(tarea_id)}, {"$unset": {"fecha_fin": ""}})
            del tarea_dict["fecha_fin"] # Para que no se intente setear a None directamente en el $set
        elif "fecha_fin" in tarea_dict and tarea_dict["fecha_fin"] is not None:
             tarea_dict["fecha_fin"] = tarea.fecha_fin # Actualizar el valor

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

# Manteniendo la opción de desactivar como en tu plantilla
async def deactivate_tarea(tarea_id: str) -> Tarea:
    try:
        # Aquí puedes establecer el estado de la tarea a 'desactivada' o 'cancelada'
        # o a un ID de estado que represente ese concepto.
        result = coll.update_one(
            {"_id": ObjectId(tarea_id)},
            {"$set": {"estado_tarea": "desactivada"}} # O a un ID de estado "desactivado"
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Tarea not found")

        return await get_tarea_by_id(tarea_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deactivating task: {str(e)}")