from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
# Imports actualizados con los nuevos Schemas
from app.models import User, UserSignup, UserResponse, UserLogin, Token
from app.database import create_db_and_tables, get_session
# Imports de seguridad actualizados (hash + verify)
from app.auth.security import hash_password, verify_password
# Import para generar el JWT
from app.auth.jwt import create_access_token

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
            "signup": "/signup",
            "login": "/login"  # Agregado a la lista para referencia
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


# ========== NUEVO ENDPOINT DE LOGIN ==========
@app.post("/login", response_model=Token)
def login(
        credentials: UserLogin,
        session: Session = Depends(get_session)
):
    """
    Autentica un usuario y devuelve un JWT token.

    Args:
        credentials: Email y password del usuario

    Returns:
        JWT token para acceder a endpoints protegidos

    Raises:
        401: Credenciales inválidas
    """
    # 1. Busca el usuario por email
    user = session.exec(
        select(User).where(User.email == credentials.email)
    ).first()

    # 2. Verifica que el usuario existe
    if not user:
        # Nota de seguridad: Es mejor decir "Email o contraseña incorrectos"
        # para no dar pistas de qué emails existen.
        raise HTTPException(
            status_code=401,
            detail="Email o contraseña incorrectos"
        )

    # 3. Verifica la contraseña
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Email o contraseña incorrectos"
        )

    # 4. Verifica que el usuario está activo (opcional pero recomendado)
    if not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="Usuario inactivo"
        )

    # 5. Crea el JWT token
    access_token = create_access_token(
        data={"sub": user.email}  # "sub" = subject (estándar JWT)
    )

    return Token(access_token=access_token)