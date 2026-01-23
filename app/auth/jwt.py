"""
Generación y validación de JWT tokens.
Maneja tanto la criptografía (crear/verificar) como la inyección de dependencias.
"""
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv

# Imports de Criptografía
from jose import JWTError, jwt

# Imports de FastAPI y Base de Datos
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from app.models import User
from app.database import get_session

load_dotenv()

# Configuración JWT
SECRET_KEY = os.getenv("SECRET_KEY", "tu-super-secreto-cambiar-en-produccion")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Define que el token viene del endpoint "/login"
# Esto es lo que hace que Swagger muestre el botón "Authorize"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ========== FUNCIONES DE LÓGICA PURA (Matemáticas) ==========

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un JWT token firmado.
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
    Decodifica el token y extrae el email (sin tocar la DB).
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None


# ========== DEPENDENCIA DE SEGURIDAD (El Guardia) ==========

def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session)
) -> User:
    """
    Dependencia que verifica el JWT y devuelve el usuario actual.
    Esta función es la "puerta blindada" de tus endpoints protegidos.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. Verifica la firma criptográfica
    email = verify_token(token)
    if email is None:
        raise credentials_exception

    # 2. Busca al usuario en la base de datos
    user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if user is None:
        raise credentials_exception

    # 3. Verifica si está activo (Regla de negocio)
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    return user