# Documentación Técnica - Mediconecta

## Índice
1. [Introducción](#introducción)
2. [Autenticación JWT](#autenticación-jwt)
3. [APIs REST](#apis-rest)
4. [Servicios Externos](#servicios-externos)
5. [Configuración y Despliegue](#configuración-y-despliegue)

---

## Introducción

**Mediconecta** es una aplicación web desarrollada en Django para la gestión de servicios médicos, que incluye:
- Gestión de médicos y pacientes
- Sistema de citas médicas
- Integración con APIs externas de salud
- Autenticación segura por tokens JWT

---

## Autenticación JWT

### Configuración

El sistema utiliza **JWT (JSON Web Tokens)** como método principal de autenticación:

- **Access Token:** 60 minutos
- **Refresh Token:** 7 días
- **Algoritmo:** HS256
- **Rotación automática:** Habilitada
- **Blacklist:** Habilitada para tokens revocados

### Endpoints de Autenticación

#### 1. Obtener Token (Login)

**POST** `/api/auth/token/`

Obtiene tokens de acceso y refresh usando credenciales (`username`, `password`).

#### 2. Renovar Token

**POST** `/api/auth/token/refresh/`

Renueva el token de acceso usando el refresh token.

#### 3. Registrar Usuario

**POST** `/api/auth/register/`

Registra un nuevo usuario y devuelve tokens automáticamente. Campos requeridos: `username`, `email`, `password`. Opcionales: `first_name`, `last_name`.

#### 4. Cerrar Sesión

**POST** `/api/auth/logout/`

Invalida el refresh token. Requiere autenticación JWT en header y `refresh_token` en el body.

#### 5. Perfil de Usuario

**GET** `/api/auth/profile/`

Obtiene el perfil del usuario autenticado. Requiere autenticación JWT.

#### 6. Verificar Token

**POST** `/api/auth/token/verify/`

Verifica si un token es válido. Requiere campo `token` en el body.

### Uso de Tokens

Para usar las APIs protegidas, incluye el header: `Authorization: Bearer <tu_access_token>`

### Manejo de Errores

| Error | Response |
|-------|----------|
| Token expirado | `{"detail": "Token is invalid or expired"}` |
| Token inválido | `{"detail": "Given token not valid for any token type"}` |
| Sin autorización | `{"detail": "Authentication credentials were not provided."}` |

---

## APIs REST

### Autenticación Soportada

1. **JWT (Recomendado)** - Token Bearer en header
2. **Sesión** - Para navegadores web
3. **HTTP Basic** - Para aplicaciones cliente

### Formato de Respuesta

Todas las APIs devuelven JSON con paginación (campos: `count`, `next`, `previous`, `results`).

### Códigos de Estado

| Código | Descripción |
|--------|-------------|
| 200 OK | Solicitud exitosa |
| 201 Created | Recurso creado |
| 400 Bad Request | Datos inválidos |
| 401 Unauthorized | No autenticado |
| 403 Forbidden | No autorizado |
| 404 Not Found | Recurso no encontrado |
| 500 Internal Server Error | Error del servidor |

---

## API de Médicos

**Base URL:** `/medicos/api/`

### Endpoints

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/medicos/` | Listar todos los médicos |
| GET | `/medicos/{id}/` | Obtener médico específico |
| POST | `/medicos/` | Crear nuevo médico |
| PUT | `/medicos/{id}/` | Actualizar médico |
| DELETE | `/medicos/{id}/` | Eliminar médico |
| GET | `/medicos/disponibles/` | Médicos disponibles |
| GET | `/medicos/por_especialidad/` | Médicos agrupados por especialidad |

### Parámetros de Consulta

- `especialidad` - Filtrar por especialidad
- `disponible` - Filtrar por disponibilidad (true/false)
- `search` - Búsqueda por nombre o especialidad

---

## API de Pacientes

**Base URL:** `/pacientes/api/`

### Endpoints

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/pacientes/` | Listar todos los pacientes |
| GET | `/pacientes/{id}/` | Obtener paciente específico |
| POST | `/pacientes/` | Crear nuevo paciente |
| PUT | `/pacientes/{id}/` | Actualizar paciente |
| DELETE | `/pacientes/{id}/` | Eliminar paciente |
| GET | `/pacientes/estadisticas/` | Estadísticas de pacientes |
| GET | `/pacientes/con_alergias/` | Pacientes con alergias |
| GET | `/pacientes/{id}/historial_medico/` | Historial médico |

### Parámetros de Consulta

- `search` - Búsqueda por nombre, RUT o teléfono
- `grupo_sanguineo` - Filtrar por grupo sanguíneo
- `edad_min` - Edad mínima
- `edad_max` - Edad máxima

---

## API de Especialidades

**Base URL:** `/medicos/api/especialidades/`

### Endpoints

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/especialidades/` | Listar especialidades |
| GET | `/especialidades/{id}/` | Obtener especialidad específica |
| GET | `/especialidades/{id}/medicos/` | Médicos de una especialidad |

---

## Servicios Externos

### 1. OpenFDA API - Medicamentos

**API Externa:** `https://api.fda.gov/drug/label.json`

**Endpoint Interno:** `/servicios-externos/medicamentos/`

**Datos Obtenidos:**
- Nombre del medicamento
- Principio activo
- Fabricante
- Descripción
- Indicaciones
- Efectos secundarios

**Cache:** 1 hora

### 2. Disease.sh API - Estadísticas de Salud

**API Externa:** `https://disease.sh/v3/covid-19`

**Endpoints Internos:**
- `/servicios-externos/estadisticas-salud/` - Vista principal
- `/servicios-externos/api/estadisticas-globales/` - Estadísticas globales
- `/servicios-externos/api/estadisticas-pais/` - Estadísticas por país

**Datos Obtenidos:**
- Casos totales, activos, recuperados, fallecidos
- Estadísticas por país

**Cache:** 30 minutos

### 3. Base de Datos Nutricional

**Endpoint Interno:** `/servicios-externos/nutricion/`

**Datos Obtenidos:**
- Calorías
- Macronutrientes (proteínas, carbohidratos, grasas)
- Fibra y azúcares
- Vitaminas y minerales

**Almacenamiento:** Base de datos local

---

## Configuración y Despliegue

**Elige UNO de los siguientes métodos según tu necesidad:**

### Opción 1: Instalación Local (Desarrollo)

```bash
# 1. Clonar repositorio
git clone <url-repositorio>
cd mediconecta-django

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp env.example .env
# Editar .env con tus valores

# 5. Migraciones
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Cargar datos de especialidades
python manage.py loaddata medicos/fixtures/especialidades.json

# 8. Ejecutar servidor
python manage.py runserver
```

### Opción 2: Despliegue con Docker (Desarrollo con contenedores)

```bash
# Construir imagen
docker-compose build

# Ejecutar contenedor
docker-compose up -d

# Migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser
```

### Opción 3: Despliegue en Railway (Producción)

1. Conectar repositorio de GitHub
2. Configurar variables de entorno en Railway:
   - `DJANGO_SECRET_KEY`
   - `DJANGO_DEBUG=0`
   - `DJANGO_ALLOWED_HOSTS=tu-dominio.railway.app`
3. Railway detectará automáticamente Django
4. Las migraciones se ejecutan automáticamente con `entrypoint.sh`

---

## Variables de Entorno

### Configuración Segura

El proyecto incluye un archivo `env.example` con variables de ejemplo. Para configurar:

```bash
# 1. Copiar el archivo de ejemplo
cp env.example .env

# 2. Generar una SECRET_KEY única
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 3. Editar .env con tus valores reales
# NUNCA compartas el archivo .env (ya está protegido en .gitignore)
```

**Variables principales:**
- `DJANGO_SECRET_KEY` - Clave secreta única (generada)
  - ⚠️ **Cada entorno debe tener su propia clave**
  - ⚠️ **NUNCA cambies la de producción sin avisar** - invalida todas las sesiones
- `DJANGO_DEBUG` - `1` para desarrollo, `0` para producción
- `DJANGO_ALLOWED_HOSTS` - Hosts permitidos (ej: `localhost,127.0.0.1`)
- `DJANGO_TIME_ZONE` - Zona horaria (ej: `America/Santiago`)
- `DATABASE_URL` - Solo para PostgreSQL en producción

**Nota sobre SECRET_KEY:**
- Tu clave local es diferente a la de producción
- Cambiar tu clave local NO afecta producción
- Cambiar la clave de producción invalida todas las sesiones y tokens JWT activos

## Comandos Útiles (Opcionales)

Estos comandos son útiles después de la instalación:

```bash
# Limpiar cache
python scripts/clean_cache.py  # Linux/Mac
powershell scripts/clean_cache.ps1  # Windows

# Generar datos de prueba
python scripts/generate_test_data.py

# Recolectar archivos estáticos (solo para producción)
python manage.py collectstatic --noinput

# Ejecutar tests
python manage.py test
```

---

## Flujo de Autenticación Completo

1. **Registro:** POST `/api/auth/register/` - Devuelve tokens automáticamente
2. **Usar APIs:** Incluir `Authorization: Bearer <access_token>` en headers
3. **Renovar Token:** POST `/api/auth/token/refresh/` cuando expire (60 min)
4. **Cerrar Sesión:** POST `/api/auth/logout/` para invalidar refresh token

---

## Seguridad

### Compartir el Proyecto de Forma Segura

**✅ Lo que SÍ debes compartir:**
- El archivo `env.example` - Contiene solo ejemplos sin datos reales
- Código fuente en Git
- Documentación

**❌ Lo que NUNCA debes compartir:**
- El archivo `.env` - Contiene tus claves secretas reales
- El archivo `db.sqlite3` - Puede contener datos sensibles
- Tokens o API keys en código
- Contraseñas en texto plano

**🔐 Cómo compartir con otros desarrolladores:**
1. Suben el repositorio a Git (`.env` ya está en `.gitignore`)
2. Comparten el archivo `env.example` (incluido en Git)
3. Cada desarrollador copia `env.example` a `.env` localmente
4. Cada uno genera sus propias claves secretas

### Endpoints Públicos (sin autenticación)

- `/api/auth/register/` - Registro de usuarios
- `/api/auth/token/` - Obtener token
- `/api/auth/token/verify/` - Verificar token

### Endpoints Protegidos (requieren JWT)

- Todas las APIs de médicos (`/medicos/api/`)
- Todas las APIs de pacientes (`/pacientes/api/`)
- Todas las APIs de especialidades (`/medicos/api/especialidades/`)
- Perfil de usuario (`/api/auth/profile/`)
- Logout (`/api/auth/logout/`)


---

## Soporte y Contacto

Para más información, reportar bugs o solicitar features, contacta al equipo de desarrollo.

**Proyecto:** Programación Web (PGY3221)  
**Aplicación:** Mediconecta Backend

---

## Changelog

### v1.1 (Actual)
- ✓ Autenticación JWT implementada
- ✓ Token blacklist configurado
- ✓ APIs REST completas para médicos y pacientes
- ✓ Integración con APIs externas de salud
- ✓ Soporte para PostgreSQL y SQLite
- ✓ Deploy automatizado en Railway

### v1.0
- ✓ Sistema básico de gestión médica
- ✓ Modelos de médicos, pacientes y citas
- ✓ Panel de administración Django

