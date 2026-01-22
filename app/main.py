from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from app.models import User, UserSignup, UserResponse
from app.database import create_db_and_tables, get_session
from app.auth.security import hash_password

app = FastAPI(
    title="Auth & Fraud Detection API",
    description="Sistema de autenticación con detección de anomalías ML",
    version="1.0.0"
)


# Evento de startup: crea las tablas si no existen
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {
        "message": "Auth Service is running",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "signup": "/signup"
        }
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "auth-fraud-detection"
    }


@app.post("/signup", response_model=UserResponse, status_code=201)
def signup(
        user_data: UserSignup,
        session: Session = Depends(get_session)
):
    """
    Registra un nuevo usuario en la base de datos.

    Validaciones:
    - Email único
    - Username único
    - Password hasheado antes de guardar
    """
    # 1. Verifica si el email ya existe
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email ya registrado"
        )

    # 2. Verifica si el username ya existe
    existing_username = session.exec(
        select(User).where(User.username == user_data.username)
    ).first()

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username ya existe"
        )

    # 3. Crea el usuario con password hasheado
    hashed_pwd = hash_password(user_data.password)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd
    )

    # 4. Guarda en la base de datos
    session.add(new_user)
    session.commit()
    session.refresh(new_user)  # Obtiene el ID generado

    return new_user