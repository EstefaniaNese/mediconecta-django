# Programación Web (PGY3221)  
## Desarrollando el BackEnd de nuestra aplicación Web

**Mediconecta** - Sistema de Gestión Médica

## 📚 Documentación

Para información completa sobre APIs, autenticación JWT, configuración y despliegue, consulta:

**[Documentacion.md](./Documentacion.md)**

## 🚀 Inicio Rápido

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar variables de entorno (copiar ejemplo y editar)
cp env.example .env
# Edita .env con tus valores reales (ver Documentacion.md)

# 3. Ejecutar migraciones
python manage.py migrate

# 4. Crear superusuario
python manage.py createsuperuser

# 5. Ejecutar servidor
python manage.py runserver
```

## 🔐 Seguridad

**Archivo `env.example`:** Contiene ejemplos de variables de entorno  
**Archivo `.env`:** Tus valores reales (NUNCA lo subas a Git - ya está protegido)

## 📦 Stack Tecnológico

- **Framework:** Django 5.2
- **API:** Django REST Framework
- **Autenticación:** JWT (Simple JWT)
- **Base de datos:** SQLite (dev) / PostgreSQL (prod)
- **Deploy:** Railway / Docker

