from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm  # <--- IMPORTANTE
from sqlmodel import Session, select

# Imports de Schemas (Modelos de datos)
from app.models import User, UserSignup, UserResponse, Token
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

# Evento de startup
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
            "me": "/me"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "auth-fraud-detection"
    }

# ========== REGISTRO DE USUARIOS ==========
@app.post("/signup", response_model=UserResponse, status_code=201)
def signup(
        user_data: UserSignup,
        session: Session = Depends(get_session)
):
    # 1. Verifica si el email ya existe
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    # 2. Verifica si el username ya existe
    existing_username = session.exec(
        select(User).where(User.username == user_data.username)
    ).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username ya existe")

    # 3. Crea el usuario
    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd
    )

    # 4. Guarda en DB
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


# ========== LOGIN (Estándar OAuth2) ==========
@app.post("/login", response_model=Token)
def login(
    # Esto lee el formulario que envía Swagger (username/password)
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """
    Login compatible con OAuth2 (Swagger Authorize).
    Usa 'username' para enviar el email.
    """
    # 1. Busca el usuario (OJO: form_data.username contiene el email)
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

    # 3. Crea el JWT token
    access_token = create_access_token(
        data={"sub": user.email}
    )

    return Token(access_token=access_token)


# ========== ENDPOINT PROTEGIDO ==========
@app.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Devuelve los datos del usuario logueado.
    Requiere Header -> Authorization: Bearer <token>
    """
    return current_user