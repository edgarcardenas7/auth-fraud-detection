"""
Modelos Pydantic para validación de datos.

Estos modelos definen la "forma" de los datos que tu API acepta.
Pydantic valida automáticamente y convierte tipos.
"""
from pydantic import BaseModel, EmailStr, Field


class UserSignup(BaseModel):
    """
    Esquema para registro de nuevos usuarios.

    Attributes:
        username: Nombre de usuario único
        email: Email válido (Pydantic lo valida automáticamente)
        password: Contraseña (mínimo 8 caracteres)
    """
    username: str = Field(
        ...,  # Campo obligatorio
        min_length=3,
        max_length=50,
        description="Nombre de usuario único"
    )
    email: EmailStr = Field(
        ...,
        description="Email válido del usuario"
    )
    password: str = Field(
        ...,
        min_length=8,
        description="Contraseña (mínimo 8 caracteres)"
    )


class UserResponse(BaseModel):
    """
    Esquema para respuestas (sin contraseña).

    NUNCA devuelvas la contraseña en las respuestas.
    """
    username: str
    email: EmailStr
    message: str