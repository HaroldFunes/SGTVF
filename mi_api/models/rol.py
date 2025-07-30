from pydantic import BaseModel, Field
from typing import Optional

class Rol(BaseModel):
    # El _id de MongoDB se mapea a 'id' en el modelo Pydantic.
    # Es Optional porque MongoDB lo genera si no se proporciona al insertar.
    id: Optional[str] = Field(
        default=None,
        description="Identificador único del rol (ObjectId de MongoDB)"
    )
    nombre_rol: str = Field(
        default="",
        description="Nombre descriptivo del rol (ej. 'admin', 'usuario')"
    )