"""
Modelos de datos para validación (Pydantic) y base de datos (SQLModel).
"""
from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from typing import Optional
from datetime import datetime


# ========== MODELO DE BASE DE DATOS ==========
class User(SQLModel, table=True):
    """
    Tabla de usuarios en PostgreSQL.

    SQLModel combina Pydantic (validación) con SQLAlchemy (ORM).
    """
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, max_length=50)
    email: str = Field(index=True, unique=True)
    hashed_password: str  # NUNCA guardamos passwords en texto plano
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ========== SCHEMAS PARA LA API (solo validación) ==========
class UserSignup(SQLModel):
    """
    Schema para registro de usuarios (lo que recibe la API).
    """
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(SQLModel):
    """
    Schema para respuestas (lo que devuelve la API).
    NUNCA incluye la contraseña.
    """
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime