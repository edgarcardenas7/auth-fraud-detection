"""
Generación y validación de JWT tokens.
"""
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración JWT
SECRET_KEY = os.getenv("SECRET_KEY", "tu-super-secreto-cambiar-en-produccion")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un JWT token.

    Args:
        data: Información a incluir en el token (ej: {"sub": "edgar@example.com"})
        expires_delta: Tiempo de expiración (default: 30 min)

    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """
    Verifica un JWT token y extrae el email del usuario.

    Args:
        token: JWT token a verificar

    Returns:
        Email del usuario si el token es válido, None si no
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            return None

        return email

    except JWTError:
        return None