from pydantic import BaseModel, Field
from typing import Optional

class Rol(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="Identificador único del rol (ObjectId de MongoDB)"
    )
    nombre_rol: str = Field(
        default="",
        description="Nombre descriptivo del rol (ej. 'admin', 'usuario')"
    )