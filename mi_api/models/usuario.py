from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re

class Usuario(BaseModel):
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
    # Referencia a la colección Rol. Asumo que se referencia el ID del rol.
    # Si se referenciara el nombre_rol, el tipo podría ser str y la descripción cambiaría.
    rol: str = Field(
        default="",
        description="Identificador del rol asignado al usuario (FK a la colección Rol)"
    )
    
    fecha_registro: datetime = Field(
        default_factory=datetime.now,
        description="Fecha y hora de registro del usuario"
    )

    from pydantic import Field # Asegúrate de importar Field de pydantic

    password: str = Field(
        min_length=8,
        max_length=64,
        description="Contraseña del usuario, debe tener entre 8 y 64 caracteres."
    )

    @field_validator('password')
    @classmethod
    def validate_password_complexity(cls, value: str):
        if not re.search(r"[A-Z]", value):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r"\d", value):
            raise ValueError("La contraseña debe contener al menos un número.")
        if not re.search(r"[!@#$%^&*?]", value): # Agregué algunos caracteres especiales comunes
            raise ValueError("La contraseña debe contener al menos un carácter especial (!@#$%^&*?).")
        return value