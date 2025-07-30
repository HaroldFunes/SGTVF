from bson import ObjectId

def get_usuarios_with_rol_pipeline() -> list:
    """Pipeline para obtener todos los usuarios con información detallada de su rol."""
    return [
        {
            "$lookup": {
                "from": "roles",             # Colección de Rol
                "localField": "rol",         # Campo en la colección 'usuarios' (se asume que es el ID del rol)
                "foreignField": "_id",       # Campo en la colección 'roles'
                "as": "rol_info"             # Nombre del campo para el resultado del lookup
            }
        },
        {
            "$unwind": { # Deshacer el array si siempre esperas un solo rol
                "path": "$rol_info",
                "preserveNullAndEmptyArrays": True # Para incluir usuarios sin rol asignado si fuera el caso
            }
        },
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "firebase_uid": 1,
                "email": 1,
                "nombre": 1,
                "rol": {"$toString": "$rol"}, # Convertir el ID de FK a String
                "nombre_rol": "$rol_info.nombre_rol", # Extraer el nombre del rol
                "fecha_registro": 1,
                "_id": 0
            }
        },
        {"$sort": {"fecha_registro": -1}}
    ]

def get_usuario_by_id_with_rol_pipeline(usuario_id: str) -> list:
    """Pipeline para obtener un usuario específico con la información detallada de su rol."""
    return [
        {"$match": {"_id": ObjectId(usuario_id)}},
        {
            "$lookup": {
                "from": "roles",
                "localField": "rol",
                "foreignField": "_id",
                "as": "rol_info"
            }
        },
        {
            "$unwind": {
                "path": "$rol_info",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "firebase_uid": 1,
                "email": 1,
                "nombre": 1,
                "rol": {"$toString": "$rol"},
                "nombre_rol": "$rol_info.nombre_rol",
                "fecha_registro": 1,
                "_id": 0
            }
        }
    ]

def validate_usuario_exists_pipeline(usuario_id: str) -> list:
    """Pipeline para validar que un usuario existe por su ID."""
    return [
        {"$match": {"_id": ObjectId(usuario_id)}},
        {"$project": {"_id": 1}},
        {"$limit": 1}
    ]

def validate_email_exists_pipeline(email: str) -> list:
    """Pipeline para validar que un email existe."""
    return [
        {"$match": {"email": email.lower()}},
        {"$project": {"_id": 1}},
        {"$limit": 1}
    ]

def validate_firebase_uid_exists_pipeline(firebase_uid: str) -> list:
    """Pipeline para validar que un firebase_uid existe."""
    return [
        {"$match": {"firebase_uid": firebase_uid}},
        {"$project": {"_id": 1}},
        {"$limit": 1}
    ]