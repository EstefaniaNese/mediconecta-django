# Documentación de Autenticación por Token - Mediconecta

## Autenticación JWT Implementada

La aplicación ahora soporta **autenticación basada en token JWT** para todas las APIs REST, proporcionando una forma segura y escalable de autenticación.

## Endpoints de Autenticación

### 1. Obtener Token de Acceso

**POST** `/api/auth/token/`

Obtiene un token de acceso y refresh token usando credenciales de usuario.

**Parámetros:**
```json
{
    "username": "tu_usuario",
    "password": "tu_contraseña"
}
```

**Respuesta exitosa:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 2. Renovar Token

**POST** `/api/auth/token/refresh/`

Renueva el token de acceso usando el refresh token.

**Parámetros:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Respuesta:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 3. Verificar Token

**POST** `/api/auth/token/verify/`

Verifica si un token es válido.

**Parámetros:**
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 4. Registrar Usuario

**POST** `/api/auth/register/`

Registra un nuevo usuario y obtiene tokens automáticamente.

**Parámetros:**
```json
{
    "username": "nuevo_usuario",
    "email": "usuario@email.com",
    "password": "contraseña_segura",
    "first_name": "Nombre",
    "last_name": "Apellido"
}
```

**Respuesta:**
```json
{
    "message": "Usuario registrado exitosamente",
    "user": {
        "id": 1,
        "username": "nuevo_usuario",
        "email": "usuario@email.com",
        "first_name": "Nombre",
        "last_name": "Apellido",
        "is_staff": false
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

### 5. Cerrar Sesión

**POST** `/api/auth/logout/`

Invalida el refresh token (requiere autenticación).

**Parámetros:**
```json
{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 6. Perfil de Usuario

**GET** `/api/auth/profile/`

Obtiene el perfil del usuario autenticado (requiere token).

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Respuesta:**
```json
{
    "id": 1,
    "username": "usuario",
    "email": "usuario@email.com",
    "first_name": "Nombre",
    "last_name": "Apellido",
    "is_staff": false,
    "tipo_usuario": "medico",
    "especialidad": "Cardiología",
    "registro_colegio": "12345",
    "disponible": true
}
```

## Uso de Tokens en APIs REST

### Configuración del Header

Para usar las APIs REST con autenticación por token, incluye el header:

```
Authorization: Bearer <tu_token_de_acceso>
```

### Ejemplos de Uso

#### 1. Listar Médicos
```bash
curl -X GET "http://localhost:8000/medicos/api/medicos/" \
     -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

#### 2. Crear Paciente
```bash
curl -X POST "http://localhost:8000/pacientes/api/pacientes/" \
     -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
     -H "Content-Type: application/json" \
     -d '{
       "rut": "12345678-9",
       "telefono": "+56912345678",
       "grupo_sanguineo": "O+"
     }'
```

#### 3. Obtener Estadísticas de Pacientes
```bash
curl -X GET "http://localhost:8000/pacientes/api/pacientes/estadisticas/" \
     -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

## Configuración de Tokens

### Duración de Tokens

- **Access Token:** 60 minutos
- **Refresh Token:** 7 días
- **Rotación automática:** Habilitada
- **Blacklist:** Habilitada para tokens revocados

### Algoritmo de Firma

- **Algoritmo:** HS256
- **Clave de firma:** SECRET_KEY de Django
- **Header:** `Authorization: Bearer <token>`

## Flujo de Autenticación Completo

### 1. Registro de Usuario
```bash
# 1. Registrar usuario
curl -X POST "http://localhost:8000/api/auth/register/" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "doctor_garcia",
       "email": "dr.garcia@hospital.com",
       "password": "password123",
       "first_name": "Carlos",
       "last_name": "García"
     }'
```

### 2. Obtener Token (si ya tienes cuenta)
```bash
# 2. Obtener token
curl -X POST "http://localhost:8000/api/auth/token/" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "doctor_garcia",
       "password": "password123"
     }'
```

### 3. Usar APIs con Token
```bash
# 3. Usar API con token
curl -X GET "http://localhost:8000/medicos/api/medicos/disponibles/" \
     -H "Authorization: Bearer <access_token>"
```

### 4. Renovar Token (cuando expire)
```bash
# 4. Renovar token
curl -X POST "http://localhost:8000/api/auth/token/refresh/" \
     -H "Content-Type: application/json" \
     -d '{
       "refresh": "<refresh_token>"
     }'
```

## Seguridad Implementada

### ✅ Características de Seguridad

1. **Tokens JWT firmados** con clave secreta
2. **Expiración automática** de tokens
3. **Rotación de refresh tokens** para mayor seguridad
4. **Blacklist de tokens** revocados
5. **Validación de tokens** en cada request
6. **Información del usuario** en el token
7. **Manejo seguro de errores**

### ✅ APIs Protegidas

Todas las APIs REST propias están protegidas:

- **API de Médicos:** `/medicos/api/`
- **API de Pacientes:** `/pacientes/api/`
- **API de Especialidades:** `/medicos/api/especialidades/`

### ✅ Endpoints Públicos

Los siguientes endpoints no requieren autenticación:

- **Registro:** `/api/auth/register/`
- **Login:** `/api/auth/token/`
- **Verificar token:** `/api/auth/token/verify/`

## Manejo de Errores

### Token Expirado
```json
{
    "detail": "Token is invalid or expired"
}
```

### Token Inválido
```json
{
    "detail": "Given token not valid for any token type"
}
```

### Sin Autorización
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Mejores Prácticas

### 1. Almacenamiento de Tokens
- **Access Token:** Almacenar en memoria (no persistir)
- **Refresh Token:** Almacenar de forma segura (localStorage con HTTPS)

### 2. Renovación Automática
- Renovar tokens antes de que expiren
- Usar refresh token para obtener nuevo access token

### 3. Manejo de Errores
- Verificar códigos de estado HTTP
- Manejar tokens expirados automáticamente

### 4. Seguridad
- Usar HTTPS en producción
- No exponer tokens en logs
- Implementar rate limiting

## Ejemplo de Cliente JavaScript

```javascript
// Configurar token
const token = localStorage.getItem('access_token');
const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
};

// Hacer request
fetch('/medicos/api/medicos/', {
    method: 'GET',
    headers: headers
})
.then(response => {
    if (response.status === 401) {
        // Token expirado, renovar
        return refreshToken();
    }
    return response.json();
})
.then(data => console.log(data));

// Función para renovar token
function refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    return fetch('/api/auth/token/refresh/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refreshToken })
    })
    .then(response => response.json())
    .then(data => {
        localStorage.setItem('access_token', data.access);
        // Reintentar request original
    });
}
```

## Conclusión

La implementación de autenticación por token JWT proporciona:

- ✅ **Seguridad robusta** con tokens firmados
- ✅ **Escalabilidad** para aplicaciones cliente
- ✅ **Flexibilidad** para diferentes tipos de clientes
- ✅ **Manejo automático** de expiración y renovación
- ✅ **Compatibilidad** con estándares JWT

Todas las APIs REST propias ahora soportan autenticación por token de forma segura y eficiente.
