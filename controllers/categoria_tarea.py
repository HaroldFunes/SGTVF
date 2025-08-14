from models.categoria_tarea import CategoriaTarea
from utils.mongodb import get_collection
from fastapi import HTTPException
from bson import ObjectId

coll = get_collection("categorias_tarea")

async def create_categoria_tarea(categoria_tarea: CategoriaTarea) -> CategoriaTarea:
    try:
        categoria_tarea.nombre_categoria = categoria_tarea.nombre_categoria.strip().lower()

        existing_category = coll.find_one({"nombre_categoria": categoria_tarea.nombre_categoria})
        if existing_category:
            raise HTTPException(status_code=400, detail="Task category with this name already exists")

        categoria_tarea_dict = categoria_tarea.model_dump(exclude={"id"})
        inserted = coll.insert_one(categoria_tarea_dict)
        categoria_tarea.id = str(inserted.inserted_id)
        return categoria_tarea
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating task category: {str(e)}")

async def get_categorias_tarea() -> list[CategoriaTarea]:
    try:
        categorias_tarea = []
        for doc in coll.find():
            doc['id'] = str(doc['_id'])
            del doc['_id']
            categorias_tarea.append(CategoriaTarea(**doc))
        return categorias_tarea
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching task categories: {str(e)}")

async def get_categoria_tarea_by_id(categoria_tarea_id: str) -> CategoriaTarea:
    try:
        doc = coll.find_one({"_id": ObjectId(categoria_tarea_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Task category not found")

        doc['id'] = str(doc['_id'])
        del doc['_id']
        return CategoriaTarea(**doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching task category: {str(e)}")

async def update_categoria_tarea(categoria_tarea_id: str, categoria_tarea: CategoriaTarea) -> CategoriaTarea:
    try:
        categoria_tarea.nombre_categoria = categoria_tarea.nombre_categoria.strip().lower()

        existing_category = coll.find_one({"nombre_categoria": categoria_tarea.nombre_categoria, "_id": {"$ne": ObjectId(categoria_tarea_id)}})
        if existing_category:
            raise HTTPException(status_code=400, detail="Task category with this name already exists")

        result = coll.update_one(
            {"_id": ObjectId(categoria_tarea_id)},
            {"$set": categoria_tarea.model_dump(exclude={"id"})}
        )
        if result.modified_count == 0:
            if coll.find_one({"_id": ObjectId(categoria_tarea_id)}) is None:
                raise HTTPException(status_code=404, detail="Task category not found")
            return await get_categoria_tarea_by_id(categoria_tarea_id)
        
        return await get_categoria_tarea_by_id(categoria_tarea_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating task category: {str(e)}")

async def delete_categoria_tarea(categoria_tarea_id: str):
    try:
        result = coll.delete_one({"_id": ObjectId(categoria_tarea_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Task category not found")
        return {"message": "Task category deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting task category: {str(e)}")