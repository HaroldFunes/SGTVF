from bson import ObjectId

def get_roles_pipeline() -> list:
    """Pipeline para obtener todos los roles."""
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
    """Pipeline para obtener un rol específico por su ID."""
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
    """Pipeline para validar que un rol existe por su ID."""
    return [
        {"$match": {"_id": ObjectId(rol_id)}},
        {"$project": {"_id": 1}},
        {"$limit": 1}
    ]

def validate_rol_by_name_exists_pipeline(nombre_rol: str) -> list:
    """Pipeline para validar que un rol existe por su nombre (case-insensitive)."""
    return [
        {"$match": {"nombre_rol": nombre_rol.lower()}},
        {"$project": {"_id": 1}},
        {"$limit": 1}
    ]