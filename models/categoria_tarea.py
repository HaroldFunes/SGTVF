from pydantic import BaseModel, Field
from typing import Optional

class CategoriaTarea(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="Identificador único de la categoría de la tarea (ObjectId de MongoDB)"
    )
    nombre_categoria: str = Field(
        default="",
        description="Nombre descriptivo de la categoría de la tarea (ej. 'Desarrollo', 'Diseño', 'Pruebas')"
    )
    descripcion: str = Field(
        default="",
        description="Descripción detallada de la categoría de la tarea"
    )