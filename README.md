# Auth & Fraud Detection API

Sistema de autenticación con detección de anomalías en tiempo real usando Machine Learning.

![Python](https://img.shields.io/badge/python-3.11--3.14-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🚀 Características

- ✅ Registro y autenticación de usuarios (OAuth2 estándar)
- ✅ Validación automática con Pydantic v2
- ✅ Passwords hasheados con PBKDF2-SHA256
- ✅ JWT tokens con expiración configurable
- ✅ Endpoints protegidos con dependencias reutilizables
- ✅ **Detección de anomalías en tiempo real** con scikit-learn
- ✅ Tracking de logins (IP, user-agent, timestamp)
- ✅ Dashboard administrativo para monitoreo de seguridad
- ✅ Arquitectura modular con APIRouter
- ✅ Dockerizado y listo para producción
- ✅ Documentación interactiva con Swagger UI

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI**: Framework moderno para APIs
- **Python 3.11+**: Lenguaje principal
- **Pydantic v2**: Validación de datos
- **SQLModel**: ORM (SQLAlchemy + Pydantic)

### Base de Datos
- **PostgreSQL 15**: Base de datos relacional
- **Tablas**: `users`, `login_attempts`

### Machine Learning
- **scikit-learn**: Isolation Forest para detección de anomalías
- **Features**: hora del día, día de la semana, frecuencia de logins

### Seguridad
- **PBKDF2-SHA256**: Hashing de passwords (NIST standard)
- **JWT**: Tokens de autenticación (30 min expiration)
- **OAuth2**: Flujo estándar compatible con frontends

### Infraestructura
- **Docker**: Contenedores para FastAPI + PostgreSQL
- **docker-compose**: Orquestación local
- **uvicorn**: Servidor ASGI

## 🔐 Seguridad

### Password Hashing
Usa **PBKDF2-SHA256** en lugar de bcrypt por:
- ✅ Compatible con Python 3.14+
- ✅ Compatible con Apple Silicon (M-series)
- ✅ Estándar NIST
- ✅ Usado por Django y Flask-Security
- ✅ Sin dependencias de compilación en C

### Detección de Anomalías
El sistema usa **Isolation Forest** para detectar:
- Logins en horarios inusuales (ej. 3am)
- Accesos en días atípicos (ej. domingos)
- Patrones de frecuencia sospechosos

**Scores**:
- `> 0`: Normal
- `< -0.5`: Sospechoso
- `< -0.7`: Altamente anómalo

## 📦 Instalación

### Opción 1: Con Docker (Recomendado)
```bash
# Clona el repositorio
git clone https://github.com/edgarcardenas7/auth-fraud-detection.git
cd auth-fraud-detection

# Copia las variables de entorno
cp .env.example .env

# Levanta los servicios
docker-compose up -d

# La API estará en http://localhost:8000
```

### Opción 2: Local (sin Docker)
```bash
# Clona el repositorio
git clone https://github.com/edgarcardenas7/auth-fraud-detection.git
cd auth-fraud-detection

# Crea entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instala dependencias
pip install -r requirements.txt

# Crea base de datos PostgreSQL
createdb auth_db

# Configura variables de entorno
cp .env.example .env
# Edita .env con tus credenciales

# Ejecuta el servidor
uvicorn app.main:app --reload
```

## 🔗 Endpoints

### Autenticación
- `POST /auth/signup` - Registrar nuevo usuario
- `POST /auth/login` - Login (OAuth2 form)

### Usuarios
- `GET /users/me` - Info del usuario autenticado
- `GET /users/me/login-history` - Historial de logins

### Admin
- `GET /admin/anomalies` - Logins sospechosos detectados

### Utilidades
- `GET /` - Info de la API
- `GET /health` - Health check
- `GET /docs` - Documentación interactiva (Swagger)
- `GET /redoc` - Documentación alternativa

## 🧪 Uso

### 1. Registro
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "edgar",
    "email": "edgar@example.com",
    "password": "secreto123"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=edgar@example.com&password=secreto123"
```

### 3. Acceder a endpoint protegido
```bash
curl http://localhost:8000/users/me \
  -H "Authorization: Bearer <tu-token-jwt>"
```

## 🏗️ Arquitectura
```
┌─────────────────────────────────────────────────┐
│                  CLIENTE                         │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│             FastAPI (main.py)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │   Auth   │  │  Users   │  │  Admin   │      │
│  │  Router  │  │  Router  │  │  Router  │      │
│  └──────────┘  └──────────┘  └──────────┘      │
└────────────────┬────────────────────────────────┘
                 │
         ┌───────┴───────┐
         │               │
         ▼               ▼
┌─────────────┐  ┌─────────────┐
│  Security   │  │     ML      │
│  (PBKDF2)   │  │  Detector   │
└─────────────┘  └─────────────┘
         │               │
         └───────┬───────┘
                 ▼
┌─────────────────────────────────────────────────┐
│           PostgreSQL (SQLModel)                  │
│  ┌─────────┐  ┌─────────────────┐              │
│  │  users  │  │ login_attempts  │              │
│  └─────────┘  └─────────────────┘              │
└─────────────────────────────────────────────────┘
```

## 📊 Progreso del Proyecto

- [x] Setup inicial con FastAPI
- [x] Validación con Pydantic
- [x] Conexión a PostgreSQL
- [x] Sistema de registro
- [x] Sistema de login con JWT
- [x] Endpoints protegidos
- [x] Tracking de logins
- [x] Detección de anomalías con ML
- [x] Arquitectura modular
- [x] Dashboard administrativo
- [x] Dockerización
- [ ] Deploy en Railway/Render
- [ ] CI/CD con GitHub Actions
- [ ] Monitoring y alertas

## 🧪 Testing
```bash
# Ejecuta tests (cuando estén implementados)
pytest

# Con coverage
pytest --cov=app --cov-report=html
```

## 🚀 Deploy

### Railway
```bash
# Instala Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### Render
1. Conecta tu repositorio de GitHub
2. Selecciona "Web Service"
3. Configura las variables de entorno
4. Deploy automático

## 👨‍💻 Autor

**Edgar Cárdenas**  
Backend AI Engineer  
Guadalajara, México

- GitHub: [@edgarcardenas7](https://github.com/edgarcardenas7)
- LinkedIn: [tu-perfil](https://linkedin.com/in/tu-perfil)

## 📝 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles

## 🙏 Agradecimientos

- FastAPI por el framework increíble
- scikit-learn por las herramientas de ML
- La comunidad de Python