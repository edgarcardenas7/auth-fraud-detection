from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import datetime
from typing import List

# Imports de Schemas y Modelos
# Agregamos LoginAttempt aquí
from app.models import User, UserSignup, UserResponse, Token, LoginAttempt
from app.database import create_db_and_tables, get_session
# Imports de seguridad
from app.auth.security import hash_password, verify_password
# Imports de JWT
from app.auth.jwt import create_access_token, get_current_user

app = FastAPI(
    title="Auth & Fraud Detection API",
    description="Sistema de autenticación con detección de anomalías ML",
    version="1.0.0"
)


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
            "signup": "/signup",
            "login": "/login",
            "me": "/me",
            "history": "/me/login-history"
        }
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "auth-fraud-detection"
    }


# ========== REGISTRO ==========
@app.post("/signup", response_model=UserResponse, status_code=201)
def signup(
        user_data: UserSignup,
        session: Session = Depends(get_session)
):
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    existing_username = session.exec(select(User).where(User.username == user_data.username)).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username ya existe")

    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


# ========== LOGIN (Con Registro de Actividad) ==========
@app.post("/login", response_model=Token)
def login(
        request: Request,  # <--- NUEVO: Para obtener IP y User-Agent
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_session)
):
    """
    Login compatible con OAuth2.
    Registra IP, Hora y User-Agent para detección de anomalías.
    """
    # 1. Busca usuario
    user = session.exec(
        select(User).where(User.email == form_data.username)
    ).first()

    # 2. Verifica credenciales
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(status_code=401, detail="Usuario inactivo")

    # 3. REGISTRO DE INTENTO DE LOGIN (NUEVO)
    # Antes de dar el token, guardamos la evidencia
    now = datetime.utcnow()
    login_attempt = LoginAttempt(
        user_id=user.id,
        timestamp=now,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent", "unknown"),
        success=True,
        hour_of_day=now.hour,
        day_of_week=now.weekday()
    )

    session.add(login_attempt)
    session.commit()

    # 4. Genera Token
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token)


# ========== ENDPOINTS PROTEGIDOS ==========
@app.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/me/login-history")
def get_login_history(
        current_user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
        limit: int = 10
):
    """
    Devuelve los últimos logins del usuario.
    Sirve para ver qué datos está aprendiendo el modelo.
    """
    attempts = session.exec(
        select(LoginAttempt)
        .where(LoginAttempt.user_id == current_user.id)
        .where(LoginAttempt.success == True)
        .order_by(LoginAttempt.timestamp.desc())
        .limit(limit)
    ).all()

    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "total_tracked": len(attempts),
        "recent_logins": [
            {
                "timestamp": attempt.timestamp,
                "ip": attempt.ip_address,
                "hour": attempt.hour_of_day,
                "day": attempt.day_of_week
            }
            for attempt in attempts
        ]
    }