from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Tarea(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="Identificador único de la tarea (ObjectId de MongoDB)"
    )
    id_proyecto: str = Field(
        default="",
        description="Identificador del proyecto al que pertenece la tarea (FK a la colección Proyecto)"
    )
    actividad: str = Field(
        default="",
        description="Descripción de la actividad o tarea a realizar"
    )
    fecha_fin: Optional[datetime] = Field(
        default=None,
        description="Fecha límite para la finalización de la tarea (puede ser nula)"
    )
    avance: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Porcentaje de avance de la tarea (0.0 a 100.0)"
    )
    importancia: int = Field(
        default=0,
        ge=0,
        description="Nivel de importancia de la tarea"
    )
    dificultad: str = Field(
        default="",
        description="Nivel de dificultad de la tarea (ej. 'Baja', 'Media', 'Alta')"
    )
    estado_tarea: str = Field(
        default="",
        description="Identificador del estado actual de la tarea (FK a la colección Estado_Tarea)"
    )
    categoria_tarea: str = Field(
        default="",
        description="Identificador de la categoría a la que pertenece la tarea (FK a la colección Categoria_Tarea)"
    )
    fecha_creacion: datetime = Field(
        default_factory=datetime.now,
        description="Fecha y hora de creación de la tarea"
    )
    fecha_actualizacion: datetime = Field(
        default_factory=datetime.now,
        description="Fecha y hora de la última actualización de la tarea"
    )