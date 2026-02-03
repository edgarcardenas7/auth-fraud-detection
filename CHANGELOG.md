# Changelog

Todas las cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-02

### Added
- Sistema de autenticación completo con OAuth2
- Registro de usuarios con validación Pydantic
- Login con JWT tokens (30 min expiration)
- Password hashing con PBKDF2-SHA256
- Endpoints protegidos con dependencias reutilizables
- Tracking de logins (IP, user-agent, timestamp)
- Detección de anomalías con Machine Learning (Isolation Forest)
- Dashboard administrativo para monitoreo de seguridad
- Arquitectura modular con APIRouter
- Soporte completo para Docker
- Documentación interactiva con Swagger UI
- README completo con guías de instalación y uso

### Technical Details
- FastAPI 0.100+
- PostgreSQL 15 con SQLModel
- scikit-learn para ML
- Docker + docker-compose
- 12 commits profesionales

### Security
- PBKDF2-SHA256 para password hashing (NIST standard)
- JWT tokens con SECRET_KEY configurable
- Detección de logins sospechosos en tiempo real
- Registro de auditoría de todas las sesiones

### Architecture
- Separación en capas (routes, business logic, data)
- Dependencias inyectables con FastAPI Depends
- Composición sobre herencia
- Context managers para gestión segura de recursos

## [Unreleased]

### Planned for v1.1.0
- Deploy en Railway/Render
- CI/CD con GitHub Actions
- Tests con pytest (>80% coverage)
- Endpoint para desactivar usuarios
- Notificaciones por email en logins sospechosos
- Rate limiting con Redis
- Refresh tokens para sesiones extendidas