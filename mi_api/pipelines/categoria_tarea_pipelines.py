from bson import ObjectId

def get_categorias_tarea_pipeline() -> list:
    """Pipeline para obtener todas las categorías de tarea."""
    return [
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "nombre_categoria": 1,
                "descripcion": 1,
                "_id": 0
            }
        },
        {"$sort": {"nombre_categoria": 1}}
    ]

def get_categoria_tarea_by_id_pipeline(categoria_tarea_id: str) -> list:
    """Pipeline para obtener una categoría de tarea específica por su ID."""
    return [
        {"$match": {"_id": ObjectId(categoria_tarea_id)}},
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "nombre_categoria": 1,
                "descripcion": 1,
                "_id": 0
            }
        }
    ]

def validate_categoria_tarea_exists_pipeline(categoria_tarea_id: str) -> list:
    """Pipeline para validar que una categoría de tarea existe por su ID."""
    return [
        {"$match": {"_id": ObjectId(categoria_tarea_id)}},
        {"$project": {"_id": 1}},
        {"$limit": 1}
    ]