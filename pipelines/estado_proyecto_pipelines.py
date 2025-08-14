from bson import ObjectId

def get_estados_proyecto_pipeline() -> list:
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
    return [
        {"$match": {"_id": ObjectId(estado_proyecto_id)}},
        {"$project": {"_id": 1}},
        {"$limit": 1}
    ]