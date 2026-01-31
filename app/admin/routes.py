"""
Rutas administrativas (solo para admins).
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.models import User, LoginAttempt
from app.database import get_session
from app.auth.jwt import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependencia que verifica que el usuario sea admin.

    Por ahora, simplificado: cualquier usuario autenticado es "admin".
    En producción, tendrías un campo User.is_admin.
    """
    # TODO: Agregar campo is_admin a User model
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="No tienes permisos de admin")

    return current_user


@router.get("/anomalies")
def get_anomalies(
        admin: User = Depends(get_current_admin),
        session: Session = Depends(get_session),
        limit: int = 20
):
    """
    Devuelve los últimos logins con posibles anomalías.

    Criteria simple: Logins entre 12am-6am o fines de semana.
    En producción, usarías el score del modelo ML.
    """
    # Logins sospechosos: horas raras (0-6am) o fines de semana (5=Sábado, 6=Domingo)
    suspicious_attempts = session.exec(
        select(LoginAttempt)
        .where(
            (LoginAttempt.hour_of_day < 6) |
            (LoginAttempt.day_of_week >= 5)
        )
        .order_by(LoginAttempt.timestamp.desc())
        .limit(limit)
    ).all()

    return {
        "total_suspicious": len(suspicious_attempts),
        "anomalies": [
            {
                "id": attempt.id,
                "user_id": attempt.user_id,
                "timestamp": attempt.timestamp,
                "ip": attempt.ip_address,
                "hour": attempt.hour_of_day,
                "day": attempt.day_of_week,
                "reason": (
                    "Horario nocturno" if attempt.hour_of_day < 6
                    else "Fin de semana"
                )
            }
            for attempt in suspicious_attempts
        ]
    }