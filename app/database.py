"""
Configuración de la base de datos.
"""
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Carga variables de entorno
load_dotenv()

# URL de conexión a PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/auth_db")

# Motor de conexión
engine = create_engine(DATABASE_URL, echo=True)  # echo=True muestra queries en consola

def create_db_and_tables():
    """
    Crea todas las tablas en la base de datos.
    Se ejecuta al iniciar la app.
    """
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """
    Genera una sesión de DB para cada request.
    FastAPI la cerrará automáticamente al terminar.
    """
    with Session(engine) as session:
        yield session