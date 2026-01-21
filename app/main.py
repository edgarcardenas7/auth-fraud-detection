from fastapi import FastAPI, HTTPException
from app.models import UserSignup, UserResponse

app = FastAPI(
    title="Auth & Fraud Detection API",
    description="Sistema de autenticación con detección de anomalías ML",
    version="1.0.0"
)


@app.get("/")
def root():
    """
    Endpoint raíz - Verifica que la API está funcionando.
    """
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
    """
    Health check endpoint - Para monitoreo de sistemas.
    """
    return {
        "status": "healthy",
        "service": "auth-fraud-detection"
    }


@app.post("/signup", response_model=UserResponse)
def signup(user: UserSignup):
    """
    Registra un nuevo usuario.

    Args:
        user: Datos del usuario (username, email, password)

    Returns:
        UserResponse con confirmación (sin contraseña)

    Validaciones automáticas:
    - Email debe ser válido
    - Username debe tener 3-50 caracteres
    - Password debe tener mínimo 8 caracteres
    """
    # TODO: Aquí guardarías en la base de datos
    # Por ahora solo retornamos confirmación

    return UserResponse(
        username=user.username,
        email=user.email,
        message=f"Usuario {user.username} registrado exitosamente"
    )