from bson import ObjectId

def get_proyectos_with_estado_pipeline() -> list:
    return [
        {
            "$lookup": {
                "from": "estados_proyecto",  
                "localField": "estado",     
                "foreignField": "_id",   
                "as": "estado_info"      
            }
        },
        {
            "$unwind": { 
                "path": "$estado_info",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "nombre_proyecto": 1,
                "observaciones": 1,
                "fecha_creacion": 1,
                "fecha_actualizacion": 1,
                "estado": {"$toString": "$estado"},
                "nombre_estado": "$estado_info.nombre_estado",
                "descripcion_estado": "$estado_info.descripcion",
                "_id": 0
            }
        },
        {"$sort": {"fecha_creacion": -1}}
    ]

def get_proyecto_by_id_with_estado_pipeline(proyecto_id: str) -> list:
    return [
        {"$match": {"_id": ObjectId(proyecto_id)}},
        {
            "$lookup": {
                "from": "estados_proyecto",
                "localField": "estado",
                "foreignField": "_id",
                "as": "estado_info"
            }
        },
        {
            "$unwind": {
                "path": "$estado_info",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "nombre_proyecto": 1,
                "observaciones": 1,
                "fecha_creacion": 1,
                "fecha_actualizacion": 1,
                "estado": {"$toString": "$estado"},
                "nombre_estado": "$estado_info.nombre_estado",
                "descripcion_estado": "$estado_info.descripcion",
                "_id": 0
            }
        }
    ]

def validate_proyecto_exists_pipeline(proyecto_id: str) -> list:
    return [
        {"$match": {"_id": ObjectId(proyecto_id)}},
        {"$project": {"_id": 1}},
        {"$limit": 1}
    ]

def validate_estado_proyecto_exists_pipeline(estado_id: str) -> list:
    return [
        {"$match": {"_id": ObjectId(estado_id)}},
        {"$project": {"_id": 1}},
        {"$limit": 1}
    ]