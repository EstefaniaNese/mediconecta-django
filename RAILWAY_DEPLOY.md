# Guía de Despliegue en Railway

## 🚨 PROBLEMA CRÍTICO: Error de Conexión a Base de Datos

Si estás viendo este error:
```
django.db.utils.OperationalError: could not translate host name "postgres.railway.internal" to address: Name or service not known
```

**👉 VE INMEDIATAMENTE A: `RAILWAY_DATABASE_FIX.md`**

Este archivo contiene la solución completa paso a paso para resolver el problema de conexión a PostgreSQL.

---

## 📋 Cambios Realizados para Solucionar Error 500

### 1. Configuración de CSRF y Cookies Seguras
Se agregaron las siguientes configuraciones en `config/settings.py`:
- `CSRF_TRUSTED_ORIGINS`: Lista de orígenes confiables para CSRF
- `CSRF_COOKIE_SECURE = True`: Cookies CSRF solo por HTTPS
- `SESSION_COOKIE_SECURE = True`: Cookies de sesión solo por HTTPS

### 2. Logging Mejorado
Se agregó logging detallado para capturar errores en producción:
- Logger en `accounts/views.py` para capturar errores de login
- Configuración de logging más verbosa en `settings.py`

### 3. Ejecución Automática de Migraciones
Se crearon dos métodos para asegurar que las migraciones se ejecuten:
- **Método 1**: Archivo `railway.json` con comando de inicio personalizado
- **Método 2**: `Procfile` con comando `release`

### 4. Comando de Diagnóstico
Se creó el comando `python manage.py check_production` que verifica:
- ✓ Conexión a base de datos
- ✓ Existencia de tablas de autenticación
- ✓ Estado de migraciones
- ✓ Configuración de seguridad
- ✓ Configuración de sesiones

## 🚀 Pasos para Desplegar

### Paso 1: Hacer Commit y Push
```bash
git add .
git commit -m "fix: configuración completa para producción en Railway"
git push origin master
```

### Paso 2: Verificar en Railway
Railway desplegará automáticamente. Monitorea los logs para ver:

1. **Ejecución de migraciones**:
   ```
   Running migrations:
   No migrations to apply.
   ```

2. **Recolección de archivos estáticos**:
   ```
   Collecting static files...
   X static files copied
   ```

3. **Inicio de Gunicorn**:
   ```
   [INFO] Starting gunicorn
   [INFO] Listening at: http://0.0.0.0:8080
   ```

### Paso 3: Ejecutar Diagnóstico (Opcional)
Si el error persiste, ejecuta el comando de diagnóstico en Railway CLI:

```bash
railway run python manage.py check_production
```

O desde el Railway Dashboard → Shell:
```bash
python manage.py check_production
```

## 🔍 Verificación de Variables de Entorno en Railway

Asegúrate de que estas variables estén configuradas en Railway:

### Variables Obligatorias:
```
DJANGO_SECRET_KEY=tu-clave-secreta-generada
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=mediconecta-django-production.up.railway.app,*.railway.app
DATABASE_URL=(automática por Railway PostgreSQL)
PORT=(automática por Railway)
```

### Variables Opcionales:
```
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=contraseña-segura
```

## 🐛 Debugging de Errores 500

Si el error 500 persiste después del despliegue:

### 1. Ver Logs Completos
En Railway Dashboard → Deployments → [Latest] → Logs

Busca líneas con `[ERROR]` o `Traceback`:
```
[ERROR] 2025-10-12 ... django.request ... Internal Server Error: /accounts/login/
Traceback (most recent call last):
  ...
```

### 2. Ejecutar Comando de Diagnóstico
```bash
railway run python manage.py check_production
```

Esto mostrará exactamente qué está fallando.

### 3. Verificar Migraciones Manualmente
```bash
railway run python manage.py showmigrations
```

Si hay migraciones sin aplicar (marcadas con `[ ]`), aplícalas:
```bash
railway run python manage.py migrate
```

### 4. Crear Usuario de Prueba
Si no tienes usuarios en la base de datos:
```bash
railway run python manage.py createsuperuser
```

## 🔧 Problemas Comunes y Soluciones

### Error: "No module named 'dotenv'"
**Solución**: Asegúrate de que `python-dotenv` está en `requirements.txt`

### Error: "CSRF verification failed"
**Solución**: Ya está resuelto con `CSRF_TRUSTED_ORIGINS` en este commit

### Error: "relation does not exist"
**Solución**: Las migraciones no se ejecutaron. Verifica que el `railway.json` o `Procfile` estén configurados correctamente.

### Error 500 sin traceback en logs
**Solución**: 
1. Verifica que `DJANGO_DEBUG=0` esté configurado en Railway
2. El logging detallado ahora debería mostrar errores completos

## 📝 Notas Adicionales

- **No uses DEBUG=1 en producción**: Expone información sensible
- **Rotación de SECRET_KEY**: Si cambias la SECRET_KEY, todos los usuarios serán deslogueados
- **Backups**: Railway hace backups automáticos de PostgreSQL, pero configura backups adicionales si es crítico

## 🆘 Si Nada Funciona

1. **Redeploy desde cero**:
   - En Railway Dashboard → Settings → Redeploy

2. **Revisar la base de datos**:
   ```bash
   railway run python manage.py dbshell
   \dt  # Ver todas las tablas
   ```

3. **Verificar que PostgreSQL esté vinculado**:
   - Railway Dashboard → tu servicio → Settings → Linked Services
   - Debe aparecer PostgreSQL

4. **Compartir logs completos**: Copia el traceback completo del error 500 de los logs de Railway

---

## ✅ Checklist de Despliegue

- [ ] Variables de entorno configuradas en Railway
- [ ] Código pusheado a GitHub
- [ ] Railway desplegó correctamente (sin errores en logs)
- [ ] Migraciones aplicadas (`python manage.py check_production`)
- [ ] Archivos estáticos recolectados
- [ ] Puedes acceder a la URL de Railway
- [ ] Login funciona sin error 500
- [ ] Usuario de prueba creado

---

**Última actualización**: Octubre 12, 2025

