from bson import ObjectId

def get_tareas_pipeline() -> list:
    return [
        {
            "$lookup": {
                "from": "proyectos",        
                "localField": "id_proyecto",
                "foreignField": "_id",
                "as": "proyecto_info"
            }
        },
        {"$unwind": {"path": "$proyecto_info", "preserveNullAndEmptyArrays": True}},
        {
            "$lookup": {
                "from": "estados_tarea",   
                "localField": "estado_tarea",
                "foreignField": "_id",
                "as": "estado_tarea_info"
            }
        },
        {"$unwind": {"path": "$estado_tarea_info", "preserveNullAndEmptyArrays": True}},
        {
            "$lookup": {
                "from": "categorias_tarea", 
                "localField": "categoria_tarea",
                "foreignField": "_id",
                "as": "categoria_tarea_info"
            }
        },
        {"$unwind": {"path": "$categoria_tarea_info", "preserveNullAndEmptyArrays": True}},
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "id_proyecto": {"$toString": "$id_proyecto"},
                "nombre_proyecto": "$proyecto_info.nombre_proyecto",
                "actividad": 1,
                "fecha_fin": 1,
                "avance": 1,
                "importancia": 1,
                "dificultad": 1,
                "estado_tarea": {"$toString": "$estado_tarea"},
                "nombre_estado_tarea": "$estado_tarea_info.nombre_estado",
                "categoria_tarea": {"$toString": "$categoria_tarea"},
                "nombre_categoria_tarea": "$categoria_tarea_info.nombre_categoria",
                "fecha_creacion": 1,
                "fecha_actualizacion": 1,
                "_id": 0
            }
        },
        {"$sort": {"fecha_creacion": -1}}
    ]

def get_tarea_by_id_pipeline(tarea_id: str) -> list:
    return [
        {"$match": {"_id": ObjectId(tarea_id)}},
        {
            "$lookup": {
                "from": "proyectos",
                "localField": "id_proyecto",
                "foreignField": "_id",
                "as": "proyecto_info"
            }
        },
        {"$unwind": {"path": "$proyecto_info", "preserveNullAndEmptyArrays": True}},
        {
            "$lookup": {
                "from": "estados_tarea",
                "localField": "estado_tarea",
                "foreignField": "_id",
                "as": "estado_tarea_info"
            }
        },
        {"$unwind": {"path": "$estado_tarea_info", "preserveNullAndEmptyArrays": True}},
        {
            "$lookup": {
                "from": "categorias_tarea",
                "localField": "categoria_tarea",
                "foreignField": "_id",
                "as": "categoria_tarea_info"
            }
        },
        {"$unwind": {"path": "$categoria_tarea_info", "preserveNullAndEmptyArrays": True}},
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "id_proyecto": {"$toString": "$id_proyecto"},
                "nombre_proyecto": "$proyecto_info.nombre_proyecto",
                "actividad": 1,
                "fecha_fin": 1,
                "avance": 1,
                "importancia": 1,
                "dificultad": 1,
                "estado_tarea": {"$toString": "$estado_tarea"},
                "nombre_estado_tarea": "$estado_tarea_info.nombre_estado",
                "categoria_tarea": {"$toString": "$categoria_tarea"},
                "nombre_categoria_tarea": "$categoria_tarea_info.nombre_categoria",
                "fecha_creacion": 1,
                "fecha_actualizacion": 1,
                "_id": 0
            }
        }
    ]

def get_tareas_by_proyecto_pipeline(proyecto_id: str) -> list:
    return [
        {"$match": {"id_proyecto": ObjectId(proyecto_id)}},
        {
            "$lookup": {
                "from": "estados_tarea",
                "localField": "estado_tarea",
                "foreignField": "_id",
                "as": "estado_tarea_info"
            }
        },
        {"$unwind": {"path": "$estado_tarea_info", "preserveNullAndEmptyArrays": True}},
        {
            "$lookup": {
                "from": "categorias_tarea",
                "localField": "categoria_tarea",
                "foreignField": "_id",
                "as": "categoria_tarea_info"
            }
        },
        {"$unwind": {"path": "$categoria_tarea_info", "preserveNullAndEmptyArrays": True}},
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "id_proyecto": {"$toString": "$id_proyecto"},
                "actividad": 1,
                "fecha_fin": 1,
                "avance": 1,
                "importancia": 1,
                "dificultad": 1,
                "estado_tarea": {"$toString": "$estado_tarea"},
                "nombre_estado_tarea": "$estado_tarea_info.nombre_estado",
                "categoria_tarea": {"$toString": "$categoria_tarea"},
                "nombre_categoria_tarea": "$categoria_tarea_info.nombre_categoria",
                "fecha_creacion": 1,
                "fecha_actualizacion": 1,
                "_id": 0
            }
        },
        {"$sort": {"fecha_creacion": -1}}
    ]

def validate_tarea_exists_pipeline(tarea_id: str) -> list:
    return [
        {"$match": {"_id": ObjectId(tarea_id)}},
        {"$project": {"_id": 1}},
        {"$limit": 1}
    ]