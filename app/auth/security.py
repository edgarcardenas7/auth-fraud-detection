"""
Utilidades de seguridad: hashing con PBKDF2 (Compatible con Python 3.14).
"""
from passlib.context import CryptContext

# PBKDF2 es nativo de Python, no depende de librerías externas
# Es el mismo que usa Django - producción ready
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Convierte texto plano a hash seguro usando PBKDF2.

    PBKDF2 es recomendado por NIST y usado por Django.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica la contraseña contra el hash.
    """
    return pwd_context.verify(plain_password, hashed_password)