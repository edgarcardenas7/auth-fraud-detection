from fastapi import FastAPI
from sqlmodel import Session

# Importamos la base de datos y el motor
from app.database import create_db_and_tables, engine

# Importamos los "Jefes de Departamento" (Routers)
# OJO: Aquí importamos también la función train_detector para el arranque
from app.auth.routes import router as auth_router, train_detector
from app.users.routes import router as users_router
from app.admin.routes import router as admin_router

app = FastAPI(
    title="Auth & Fraud Detection API",
    description="Sistema de autenticación con detección de anomalías ML",
    version="1.0.0"
)

# Conectamos los departamentos al edificio principal
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)


@app.on_event("startup")
def on_startup():
    """
    Al arrancar:
    1. Crea tablas en PostgreSQL.
    2. Entrena el cerebro de IA con datos históricos.
    """
    create_db_and_tables()

    # Usamos context manager para seguridad (lo que arreglamos antes)
    with Session(engine) as session:
        train_detector(session)


@app.get("/")
def root():
    return {
        "message": "Auth & Fraud Detection API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "signup": "/auth/signup",
            "login": "/auth/login",
            "me": "/users/me",
            "history": "/users/me/login-history",
            "admin_anomalies": "/admin/anomalies"
        }
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}