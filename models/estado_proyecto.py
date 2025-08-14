from pydantic import BaseModel, Field
from typing import Optional

class EstadoProyecto(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="Identificador único del estado de proyecto (ObjectId de MongoDB)"
    )
    nombre_estado: str = Field(
        default="",
        description="Nombre descriptivo del estado del proyecto (ej. 'Pendiente', 'En Progreso', 'Finalizado')"
    )
    descripcion: str = Field(
        default="",
        description="Descripción detallada del estado del proyecto"
    )