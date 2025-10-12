# 🔧 Solución: Error 502 Bad Gateway en Railway

## ❌ Error Actual
```
GET https://mediconecta-django-production.up.railway.app/ - 502 (Bad Gateway)
```

## 🔍 Significado
El error 502 significa que Railway está recibiendo la petición pero la aplicación Django **no está respondiendo** correctamente. Esto puede ser por:

1. Gunicorn no está iniciando
2. La aplicación tiene un error al arrancar
3. Timeout (la app tarda mucho en iniciar)
4. Error en migraciones o collectstatic
5. Puerto incorrecto
6. ALLOWED_HOSTS mal configurado

---

## ✅ Soluciones Implementadas

He realizado los siguientes cambios:

### 1. Aumentado Timeout de Gunicorn
- De 120s a 180s
- Agregado `graceful-timeout` de 180s
- Más threads para manejar peticiones

### 2. Mejorado Logging
- Ahora muestra `DEBUG mode` y `ALLOWED_HOSTS` al iniciar
- Nivel de log `info` en Gunicorn

---

## 🚀 Pasos Inmediatos

### Paso 1: Commit y Push
```bash
git add .
git commit -m "fix: aumentar timeout y mejorar logging para error 502"
git push origin master
```

### Paso 2: Ver Logs en Railway

**IMPORTANTE**: Después del push, ve a Railway y mira los **Deploy Logs** completos.

Busca estas líneas específicas:

#### ✅ Lo que DEBES ver (Éxito):
```
[INFO] DEBUG mode: False
[INFO] ALLOWED_HOSTS: ['mediconecta-django-production.up.railway.app', '*.railway.app']
[INFO] Conectando a base de datos: ...@XXXX.railway.app:5432/railway
✓ DATABASE_URL configuración OK (hostname moderno)
Recolectando archivos estáticos...
X static files copied to '/app/staticfiles'
Ejecutando migraciones...
Running migrations:
  No migrations to apply.
Configuración completada. Iniciando servidor...
[INFO] Starting gunicorn 22.0.0
[INFO] Listening at: http://0.0.0.0:XXXX (PID: XXX)
[INFO] Using worker: sync
[INFO] Booting worker with pid: XXX
[INFO] Booting worker with pid: XXX
```

#### ❌ Lo que indica ERROR:
```
ERROR: Could not...
Traceback (most recent call last):
django.core.exceptions...
ModuleNotFoundError...
```

---

## 🐛 Diagnósticos Específicos

### Problema 1: ALLOWED_HOSTS Inválido

**Síntomas**: Error de "Invalid HTTP_HOST header"

**Solución**: Verifica en Railway → Variables que `DJANGO_ALLOWED_HOSTS` tenga:
```
mediconecta-django-production.up.railway.app,*.railway.app
```

Si Railway ha asignado una URL diferente, agrégala:
```
tu-url-real.up.railway.app,*.railway.app
```

### Problema 2: PORT no Configurado

**Síntomas**: Gunicorn inicia pero Railway muestra 502

**Solución**: Railway debe configurar automáticamente la variable `PORT`. Verifica:
1. Railway → tu servicio → Variables
2. Debe existir `PORT` (Railway la crea automáticamente)
3. Si no existe, **NO** la crees manualmente, Railway la maneja

### Problema 3: Migraciones Fallan

**Síntomas**: Logs muestran error en `python manage.py migrate`

**Solución**: Ejecuta manualmente en Railway CLI:
```bash
railway run python manage.py migrate --run-syncdb
```

### Problema 4: Collectstatic Falla

**Síntomas**: Error en "Recolectando archivos estáticos"

**Solución**: Verifica que `whitenoise` esté instalado:
```bash
railway run pip list | grep whitenoise
```

Si no está, debe estar en `requirements.txt`.

### Problema 5: Error de Importación

**Síntomas**: `ModuleNotFoundError` en los logs

**Solución**: Verifica que `requirements.txt` tenga todas las dependencias:
```
Django>=4.2,<5.0
gunicorn>=22.0.0
psycopg2-binary>=2.9.9
whitenoise>=6.6.0
dj-database-url>=2.1.0
python-dotenv>=1.0.0
djangorestframework>=3.14.0
djangorestframework-simplejwt>=5.3.1
```

Luego:
```bash
git add requirements.txt
git commit -m "fix: actualizar dependencias"
git push
```

---

## 🔍 Comandos de Diagnóstico

### Ver Variables de Entorno en Railway
```bash
railway run env | grep DJANGO
railway run env | grep DATABASE
railway run env | grep PORT
```

### Ejecutar Check de Django
```bash
railway run python manage.py check --deploy
```

### Verificar Conexión a DB
```bash
railway run python scripts/check_railway_db.py
```

### Ver Logs en Tiempo Real
En Railway Dashboard → tu servicio → Click en "View Logs"

---

## 🆘 Si Nada Funciona

### Opción 1: Forzar Redeploy Completo
1. Railway Dashboard → Settings → "Redeploy"
2. Espera 3-5 minutos

### Opción 2: Verificar Health Check
Railway espera que la app responda en el puerto `$PORT`. Verifica que Gunicorn esté usando ese puerto.

En `railway.json` el comando debe tener `--bind 0.0.0.0:$PORT` ✅ (ya lo tienes)

### Opción 3: Desactivar CSRF Temporalmente (SOLO PARA DEBUG)

**⚠️ ADVERTENCIA**: Solo para diagnosticar, no dejar así en producción.

Agrega temporalmente en Railway → Variables:
```
DJANGO_DEBUG=1
```

Esto mostrará el error real de Django en el navegador. **ELIMÍNALA** después de ver el error.

---

## 📋 Checklist de Verificación

- [ ] `git push` realizado con los nuevos cambios
- [ ] Railway hizo redeploy automáticamente
- [ ] Revisé los Deploy Logs completos
- [ ] Vi la línea "Starting gunicorn" en los logs
- [ ] Vi "Listening at: http://0.0.0.0:XXXX" en los logs
- [ ] La variable `PORT` existe en Railway (creada automáticamente)
- [ ] `DJANGO_ALLOWED_HOSTS` tiene el dominio correcto
- [ ] `DJANGO_DEBUG=0` en producción
- [ ] PostgreSQL está funcionando (viste que sí en los logs anteriores)

---

## 📞 Información Necesaria para Ayudarte

Si después de estos pasos el error persiste, comparte:

1. **Deploy Logs completos** (los últimos 50-100 líneas)
2. **Variables de entorno** (sin mostrar SECRET_KEY ni passwords):
   - DJANGO_DEBUG=?
   - DJANGO_ALLOWED_HOSTS=?
   - PORT=? (debe existir)
3. **URL exacta** que Railway asignó a tu servicio
4. **¿Gunicorn está iniciando?** (debe decir "Starting gunicorn" en logs)

---

**Última actualización**: Octubre 12, 2025  
**Problema**: Error 502 Bad Gateway después de conectar base de datos  
**Estado**: Esperando logs para diagnóstico específico

