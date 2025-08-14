from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re

class UsuarioSalida(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="Identificador único del usuario (ObjectId de MongoDB)"
    )
    email: str = Field(
        default="",
        description="Dirección de correo electrónico del usuario",
        #pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )
    nombre: str = Field(
        default="",
        description="Nombre completo del usuario",
        #pattern=r"^([A-Za-zÁÉÍÓÚÑáéíóúñ']+-| +)$"
    )
    rol: str = Field(
        default="",
        description="Identificador del rol asignado al usuario (FK a la colección Rol)"
    )
    
    fecha_registro: datetime = Field(
        default_factory=datetime.now,
        description="Fecha y hora de registro del usuario"
    )