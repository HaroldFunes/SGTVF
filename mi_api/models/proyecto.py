from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Proyecto(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="Identificador único del proyecto (ObjectId de MongoDB)"
    )
    nombre_proyecto: str = Field(
        default="",
        description="Nombre del proyecto"
    )
    observaciones: str = Field(
        default="",
        description="Observaciones o notas adicionales sobre el proyecto"
    )
    fecha_creacion: datetime = Field(
        default_factory=datetime.now,
        description="Fecha y hora de creación del proyecto"
    )
    fecha_actualizacion: datetime = Field(
        default_factory=datetime.now,
        description="Fecha y hora de la última actualización del proyecto"
    )
    estado: str = Field(
        default="",
        description="Identificador del estado actual del proyecto (FK a la colección Estado_Proyecto)"
    )