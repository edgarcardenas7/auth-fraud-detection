# Auth & Fraud Detection API

Sistema de autenticación con detección de anomalías usando Machine Learning.

![Python](https://img.shields.io/badge/python-3.11--3.14-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🚀 Características

- ✅ Registro y autenticación de usuarios.
- ✅ Validación automática y serialización con **Pydantic v2**.
- ✅ Seguridad avanzada: Passwords hasheados con **PBKDF2-SHA256**.
- ✅ Persistencia de datos con **SQLModel** (SQLAlchemy + Pydantic).
- ✅ Detección de anomalías en logins con **scikit-learn** (En desarrollo).
- ✅ Documentación interactiva autogenerada con **Swagger UI**.

## 🛠️ Stack Tecnológico

- **Backend**: FastAPI, Python 3.11 - 3.14
- **Base de Datos**: PostgreSQL, SQLModel
- **Seguridad**: Passlib (PBKDF2-SHA256)
- **Validación**: Pydantic
- **Machine Learning**: scikit-learn (Próximamente)

## 🔐 Seguridad e Infraestructura

Debido a requisitos de compatibilidad con arquitecturas modernas (Apple Silicon M-series) y versiones de Python 3.14+, este proyecto utiliza:

- **Password Hashing**: PBKDF2-SHA256 (estándar NIST), garantizando portabilidad y seguridad sin dependencias de compilación en C complejas.
- **Environment Management**: Uso de `.env` para proteger credenciales críticas.



## 📦 Instalación

```bash
# Clonar repositorio
git clone [https://github.com/edgarcardenas7/auth-fraud-detection.git](https://github.com/edgarcardenas7/auth-fraud-detection.git)
cd auth-fraud-detection

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En macOS/Linux
# En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Nota: Edita el archivo .env con tu DATABASE_URL de PostgreSQL