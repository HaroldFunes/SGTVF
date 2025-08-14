from bson import ObjectId

def get_usuarios_with_rol_pipeline() -> list:
    return [
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
        },
        {"$sort": {"fecha_registro": -1}}
    ]

def get_usuario_by_id_with_rol_pipeline(usuario_id: str) -> list:
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
    return [
        {"$match": {"_id": ObjectId(usuario_id)}},
        {"$project": {"_id": 1}},
        {"$limit": 1}
    ]

def validate_email_exists_pipeline(email: str) -> list:
    return [
        {"$match": {"email": email.lower()}},
        {"$project": {"_id": 1}},
        {"$limit": 1}
    ]

def validate_firebase_uid_exists_pipeline(firebase_uid: str) -> list:
    return [
        {"$match": {"firebase_uid": firebase_uid}},
        {"$project": {"_id": 1}},
        {"$limit": 1}
    ]