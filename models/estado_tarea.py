from pydantic import BaseModel, Field
from typing import Optional

class EstadoTarea(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="Identificador único del estado de la tarea (ObjectId de MongoDB)"
    )
    nombre_estado: str = Field(
        default="",
        description="Nombre descriptivo del estado de la tarea (ej. 'Pendiente', 'En Curso', 'Completada')"
    )
    descripcion: str = Field(
        default="",
        description="Descripción detallada del estado de la tarea"
    )