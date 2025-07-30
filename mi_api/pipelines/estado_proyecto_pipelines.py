from bson import ObjectId

def get_estados_proyecto_pipeline() -> list:
    """Pipeline para obtener todos los estados de proyecto."""
    return [
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "nombre_estado": 1,
                "descripcion": 1,
                "_id": 0
            }
        },
        {"$sort": {"nombre_estado": 1}}
    ]

def get_estado_proyecto_by_id_pipeline(estado_proyecto_id: str) -> list:
    """Pipeline para obtener un estado de proyecto específico por su ID."""
    return [
        {"$match": {"_id": ObjectId(estado_proyecto_id)}},
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "nombre_estado": 1,
                "descripcion": 1,
                "_id": 0
            }
        }
    ]

def validate_estado_proyecto_exists_pipeline(estado_proyecto_id: str) -> list:
    """Pipeline para validar que un estado de proyecto existe por su ID."""
    return [
        {"$match": {"_id": ObjectId(estado_proyecto_id)}},
        {"$project": {"_id": 1}},
        {"$limit": 1}
    ]