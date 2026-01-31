"""
Rutas de autenticación: signup, login.
"""
from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import datetime

from app.models import User, UserSignup, UserResponse, Token, LoginAttempt
from app.database import get_session
from app.auth.security import hash_password, verify_password
from app.auth.jwt import create_access_token
from app.fraud.detector import LoginAnomalyDetector

# Router para rutas de auth
router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

# Detector de anomalías (compartido)
# Nota: En producción, esto vendría de un singleton o servicio inyectado
anomaly_detector = LoginAnomalyDetector(contamination=0.15)


@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(
        user_data: UserSignup,
        session: Session = Depends(get_session)
):
    """Registra un nuevo usuario."""
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    existing_username = session.exec(
        select(User).where(User.username == user_data.username)
    ).first()

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


@router.post("/login", response_model=Token)
def login(
        request: Request,
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_session)
):
    """
    Login con OAuth2.
    Incluye detección de anomalías en tiempo real.
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo"
        )

    # 3. Detección de anomalías
    now = datetime.utcnow()
    login_features = {
        'hour_of_day': now.hour,
        'day_of_week': now.weekday()
    }

    is_anomaly, anomaly_score = anomaly_detector.predict(login_features)

    if is_anomaly:
        print(f"🚨 ALERTA: Login sospechoso detectado!")
        print(f"   Usuario: {user.email}")
        print(f"   IP: {request.client.host}")
        print(f"   Score: {anomaly_score:.4f}")

    # 4. Registra el intento
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

    # 5. Genera token
    access_token = create_access_token(data={"sub": user.email})

    return Token(access_token=access_token)


def train_detector(session: Session):
    """
    Función helper para entrenar el detector.
    Llamada desde main.py en startup.
    """
    all_attempts = session.exec(
        select(LoginAttempt)
        .where(LoginAttempt.success == True)
        .order_by(LoginAttempt.timestamp.desc())
        .limit(100)
    ).all()

    if all_attempts:
        training_data = [
            {
                'hour_of_day': attempt.hour_of_day,
                'day_of_week': attempt.day_of_week
            }
            for attempt in all_attempts
        ]

        anomaly_detector.train(training_data)
        print(f"🤖 Detector entrenado con {len(training_data)} logins históricos")
    else:
        print("⚠️  No hay datos históricos - detector en modo pasivo")