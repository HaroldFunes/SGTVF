from bson import ObjectId

def get_roles_pipeline() -> list:
    return [
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "nombre_rol": 1,
                "_id": 0
            }
        },
        {"$sort": {"nombre_rol": 1}}
    ]

def get_rol_by_id_pipeline(rol_id: str) -> list:
    return [
        {"$match": {"_id": ObjectId(rol_id)}},
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "nombre_rol": 1,
                "_id": 0
            }
        }
    ]

def validate_rol_exists_pipeline(rol_id: str) -> list:
    return [
        {"$match": {"_id": ObjectId(rol_id)}},
        {"$project": {"_id": 1}},
        {"$limit": 1}
    ]

def validate_rol_by_name_exists_pipeline(nombre_rol: str) -> list:
    return [
        {"$match": {"nombre_rol": nombre_rol.lower()}},
        {"$project": {"_id": 1}},
        {"$limit": 1}
    ]