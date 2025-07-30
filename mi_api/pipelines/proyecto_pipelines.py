from bson import ObjectId

def get_proyectos_with_estado_pipeline() -> list:
    """Pipeline para obtener todos los proyectos con información detallada de su estado."""
    return [
        {
            "$lookup": {
                "from": "estados_proyecto",  # Colección de Estado_Proyecto
                "localField": "estado",      # Campo en la colección 'proyectos'
                "foreignField": "_id",       # Campo en la colección 'estados_proyecto'
                "as": "estado_info"          # Nombre del campo para el resultado del lookup
            }
        },
        {
            "$unwind": { # Deshacer el array si siempre esperas un solo estado
                "path": "$estado_info",
                "preserveNullAndEmptyArrays": True # Para incluir proyectos sin estado asignado si fuera el caso
            }
        },
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "nombre_proyecto": 1,
                "observaciones": 1,
                "fecha_creacion": 1,
                "fecha_actualizacion": 1,
                "estado": {"$toString": "$estado"}, # Convertir el ID de FK a String
                "nombre_estado": "$estado_info.nombre_estado",
                "descripcion_estado": "$estado_info.descripcion",
                "_id": 0
            }
        },
        {"$sort": {"fecha_creacion": -1}}
    ]

def get_proyecto_by_id_with_estado_pipeline(proyecto_id: str) -> list:
    """Pipeline para obtener un proyecto específico con la información detallada de su estado."""
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
    """Pipeline para validar que un proyecto existe por su ID."""
    return [
        {"$match": {"_id": ObjectId(proyecto_id)}},
        {"$project": {"_id": 1}},
        {"$limit": 1}
    ]

def validate_estado_proyecto_exists_pipeline(estado_id: str) -> list:
    """Pipeline para validar que un estado de proyecto existe por su ID."""
    return [
        {"$match": {"_id": ObjectId(estado_id)}},
        {"$project": {"_id": 1}},
        {"$limit": 1}
    ]