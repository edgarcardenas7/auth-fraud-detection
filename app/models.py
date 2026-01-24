"""
Modelos de datos para validación (Pydantic) y base de datos (SQLModel).
"""
from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from typing import Optional
from datetime import datetime


# ========== MODELO DE USUARIOS (Tabla) ==========
class User(SQLModel, table=True):
    """
    Tabla de usuarios en PostgreSQL.
    """
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, max_length=50)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ========== MODELO DE INTENTOS DE LOGIN (Nueva Tabla) ==========
class LoginAttempt(SQLModel, table=True):
    """
    Tabla para registrar todos los intentos de login.
    Usada para entrenamiento del modelo de ML (Isolation Forest).
    """
    __tablename__ = "login_attempts"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(foreign_key="users.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    ip_address: str
    user_agent: Optional[str] = None
    success: bool  # True si el login fue exitoso

    # Features específicas para el Machine Learning
    hour_of_day: int = Field(default=0)  # 0-23
    day_of_week: int = Field(default=0)  # 0-6 (Lunes-Domingo)

    # Índices para que las búsquedas de historial sean rápidas
    class Config:
        indexes = [
            ("user_id", "timestamp"),
        ]


# ========== SCHEMAS PARA LA API (Validación) ==========
class UserSignup(SQLModel):
    """
    Schema para registro de usuarios.
    """
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(SQLModel):
    """
    Schema para respuestas públicas (sin password).
    """
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime


class UserLogin(SQLModel):
    """
    Schema para login (JSON legacy).
    """
    email: EmailStr
    password: str


class Token(SQLModel):
    """
    Schema para respuesta de login exitoso.
    """
    access_token: str
    token_type: str = "bearer"


class TokenData(SQLModel):
    """
    Datos extraídos del token.
    """
    email: Optional[str] = None