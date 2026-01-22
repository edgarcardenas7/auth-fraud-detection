# Auth & Fraud Detection API


Sistema de autenticación con detección de anomalías usando Machine Learning.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
## 🚀 Características

- ✅ Registro y autenticación de usuarios
- ✅ Validación automática con Pydantic
- ✅ Passwords hasheados con bcrypt
- ✅ Detección de anomalías en logins (scikit-learn)
- ✅ API REST con FastAPI
- ✅ Base de datos PostgreSQL
- ✅ Documentación automática (Swagger)

## 🛠️ Stack Tecnológico

- **Backend**: FastAPI, Python 3.11+
- **Base de Datos**: PostgreSQL, SQLModel
- **Seguridad**: Passlib (bcrypt)
- **Validación**: Pydantic
- **Machine Learning**: scikit-learn (próximamente)

## 📦 Instalación
```bash
# Clonar repositorio
git clone https://github.com/TU-USUARIO/auth-fraud-detection.git
cd auth-fraud-detection

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Crear base de datos
createdb auth_db

# Ejecutar servidor
uvicorn app.main:app --reload
```

## 🔗 Endpoints

- `GET /` - Info de la API
- `GET /health` - Health check
- `POST /signup` - Registro de usuarios
- `GET /docs` - Documentación interactiva (Swagger)

## 📊 Progreso del Proyecto

- [x] Setup inicial
- [x] Validación con Pydantic
- [x] Conexión a PostgreSQL
- [x] Registro de usuarios
- [ ] Sistema de login (JWT)
- [ ] Detección de anomalías (ML)
- [ ] Docker deployment

## 👨‍💻 Autor

**Edgar Cárdenas**  
Backend AI Engineer en formación  
[LinkedIn](tu-linkedin) | [Portfolio](tu-portfolio)

## 📝 Licencia

MIT License