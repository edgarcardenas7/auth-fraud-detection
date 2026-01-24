"""
Detección de anomalías en logins usando Isolation Forest.
"""
from sklearn.ensemble import IsolationForest
import numpy as np
from typing import List, Dict, Tuple


class LoginAnomalyDetector:
    """
    Detector de anomalías en patrones de login.

    Usa Isolation Forest para detectar logins sospechosos basándose en:
    - Hora del día (0-23)
    - Día de la semana (0-6)
    """

    def __init__(self, contamination: float = 0.1):
        """
        Args:
            contamination: % esperado de anomalías (0.1 = 10%)
        """
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.is_trained = False

    def extract_features(self, login_attempts: List[Dict]) -> np.ndarray:
        """
        Convierte login attempts en features para ML.
        Returns:
            Array numpy shape (n_samples, 2): [[hora, día], ...]
        """
        features = []
        for attempt in login_attempts:
            features.append([
                attempt['hour_of_day'],
                attempt['day_of_week']
            ])
        return np.array(features)

    def train(self, login_attempts: List[Dict]) -> bool:
        """
        Entrena el modelo con datos históricos.
        Returns:
            True si entrenó exitosamente.
        """
        if len(login_attempts) < 10:
            print(f"⚠️  Necesitas al menos 10 logins. Tienes: {len(login_attempts)}")
            return False

        X = self.extract_features(login_attempts)
        self.model.fit(X)
        self.is_trained = True

        print(f"✅ Modelo entrenado con {len(login_attempts)} logins")
        return True

    def predict(self, login_attempt: Dict) -> Tuple[bool, float]:
        """
        Predice si un login es anómalo.
        Returns:
            (is_anomaly, score)
            - is_anomaly: True si es sospechoso
            - score: Número negativo = más sospechoso
        """
        if not self.is_trained:
            return False, 0.0

        X = self.extract_features([login_attempt])

        # 1 = normal, -1 = anomalía
        prediction = self.model.predict(X)[0]

        # Score: más negativo = más anómalo
        score = self.model.score_samples(X)[0]

        is_anomaly = prediction == -1

        return is_anomaly, float(score)