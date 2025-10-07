# Documentación de APIs - Mediconecta

## APIs REST Propias

### 1. API de Médicos

**Base URL:** `/medicos/api/`

#### Endpoints disponibles:

- `GET /medicos/api/medicos/` - Listar todos los médicos
- `GET /medicos/api/medicos/{id}/` - Obtener médico específico
- `POST /medicos/api/medicos/` - Crear nuevo médico
- `PUT /medicos/api/medicos/{id}/` - Actualizar médico
- `DELETE /medicos/api/medicos/{id}/` - Eliminar médico
- `GET /medicos/api/medicos/disponibles/` - Médicos disponibles
- `GET /medicos/api/medicos/por_especialidad/` - Médicos agrupados por especialidad

#### Parámetros de consulta:
- `especialidad` - Filtrar por especialidad
- `disponible` - Filtrar por disponibilidad (true/false)
- `search` - Búsqueda por nombre o especialidad

#### Ejemplo de uso:
```bash
# Listar médicos disponibles
GET /medicos/api/medicos/?disponible=true

# Buscar médicos por especialidad
GET /medicos/api/medicos/?especialidad=Cardiología

# Buscar por nombre
GET /medicos/api/medicos/?search=Dr. García
```

### 2. API de Pacientes

**Base URL:** `/pacientes/api/`

#### Endpoints disponibles:

- `GET /pacientes/api/pacientes/` - Listar todos los pacientes
- `GET /pacientes/api/pacientes/{id}/` - Obtener paciente específico
- `POST /pacientes/api/pacientes/` - Crear nuevo paciente
- `PUT /pacientes/api/pacientes/{id}/` - Actualizar paciente
- `DELETE /pacientes/api/pacientes/{id}/` - Eliminar paciente
- `GET /pacientes/api/pacientes/estadisticas/` - Estadísticas de pacientes
- `GET /pacientes/api/pacientes/con_alergias/` - Pacientes con alergias
- `GET /pacientes/api/pacientes/{id}/historial_medico/` - Historial médico

#### Parámetros de consulta:
- `search` - Búsqueda por nombre, RUT o teléfono
- `grupo_sanguineo` - Filtrar por grupo sanguíneo
- `edad_min` - Edad mínima
- `edad_max` - Edad máxima

#### Ejemplo de uso:
```bash
# Listar pacientes con alergias
GET /pacientes/api/pacientes/con_alergias/

# Buscar pacientes por RUT
GET /pacientes/api/pacientes/?search=12345678-9

# Filtrar por grupo sanguíneo
GET /pacientes/api/pacientes/?grupo_sanguineo=O+
```

### 3. API de Especialidades

**Base URL:** `/medicos/api/`

#### Endpoints disponibles:

- `GET /medicos/api/especialidades/` - Listar especialidades
- `GET /medicos/api/especialidades/{id}/` - Obtener especialidad específica
- `GET /medicos/api/especialidades/{id}/medicos/` - Médicos de una especialidad

## APIs Externas Consumidas

### 1. OpenFDA API - Medicamentos

**URL:** `https://api.fda.gov/drug/label.json`

**Propósito:** Obtener información detallada sobre medicamentos

**Datos obtenidos:**
- Nombre del medicamento
- Principio activo
- Fabricante
- Descripción
- Indicaciones
- Efectos secundarios

**Endpoint interno:** `/servicios-externos/medicamentos/`

### 2. Disease.sh API - Estadísticas de Salud

**URL:** `https://disease.sh/v3/covid-19`

**Propósito:** Obtener estadísticas de salud globales y por país

**Datos obtenidos:**
- Casos totales
- Casos activos
- Recuperados
- Fallecidos
- Estadísticas por país

**Endpoints internos:**
- `/servicios-externos/estadisticas-salud/` - Vista principal
- `/servicios-externos/api/estadisticas-globales/` - API JSON
- `/servicios-externos/api/estadisticas-pais/` - API JSON por país

### 3. Base de Datos Nutricional

**Propósito:** Información nutricional de alimentos

**Datos obtenidos:**
- Calorías
- Macronutrientes (proteínas, carbohidratos, grasas)
- Fibra y azúcares
- Vitaminas y minerales

**Endpoint interno:** `/servicios-externos/nutricion/`

## Autenticación

Todas las APIs REST propias requieren autenticación. Se puede usar:

1. **Autenticación por sesión** (recomendado para navegadores)
2. **Autenticación básica HTTP** (para aplicaciones cliente)

## Formato de Respuesta

Las APIs devuelven datos en formato JSON con la siguiente estructura:

```json
{
    "count": 10,
    "next": "http://example.com/api/endpoint/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "nombre": "Ejemplo",
            // ... otros campos
        }
    ]
}
```

## Códigos de Estado HTTP

- `200 OK` - Solicitud exitosa
- `201 Created` - Recurso creado exitosamente
- `400 Bad Request` - Datos de entrada inválidos
- `401 Unauthorized` - No autenticado
- `403 Forbidden` - No autorizado
- `404 Not Found` - Recurso no encontrado
- `500 Internal Server Error` - Error del servidor

## Ejemplos de Uso con cURL

### Obtener lista de médicos:
```bash
curl -X GET "http://localhost:8000/medicos/api/medicos/" \
     -H "Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ="
```

### Crear un nuevo paciente:
```bash
curl -X POST "http://localhost:8000/pacientes/api/pacientes/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=" \
     -d '{
       "rut": "12345678-9",
       "telefono": "+56912345678",
       "grupo_sanguineo": "O+"
     }'
```

### Buscar medicamentos:
```bash
curl -X GET "http://localhost:8000/servicios-externos/api/medicamentos/?nombre=ibuprofeno"
```

## Configuración de Cache

Las APIs externas utilizan cache para mejorar el rendimiento:

- **Medicamentos:** Cache de 1 hora
- **Estadísticas de salud:** Cache de 30 minutos
- **Información nutricional:** Base de datos local

## Limitaciones

1. **APIs Externas:** Dependen de la disponibilidad de los servicios externos
2. **Rate Limiting:** Las APIs externas pueden tener límites de solicitudes
3. **Autenticación:** Todas las APIs propias requieren autenticación
4. **Paginación:** Las listas están paginadas (20 elementos por página por defecto)

## Soporte

Para más información o soporte técnico, contacta al equipo de desarrollo.
