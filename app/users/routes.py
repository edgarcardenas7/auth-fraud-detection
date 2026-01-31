"""
Rutas de usuarios autenticados.
"""
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.models import User, UserResponse, LoginAttempt
from app.database import get_session
from app.auth.jwt import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    """Devuelve información del usuario autenticado."""
    return current_user


@router.get("/me/login-history")
def get_login_history(
        current_user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
        limit: int = 10
):
    """Devuelve el historial de logins del usuario."""
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