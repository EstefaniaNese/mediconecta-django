# 🔧 Solución: Error de Conexión a PostgreSQL en Railway

## ❌ Error
```
django.db.utils.OperationalError: could not translate host name "postgres.railway.internal" to address: Name or service not known
```

## 🔍 Causa
Railway cambió su sistema de networking y ya no usa hostnames `.railway.internal`. La variable `DATABASE_URL` está configurada con un hostname obsoleto.

---

## ✅ Solución

### Paso 1: Verificar la Variable DATABASE_URL en Railway

1. Ve a tu proyecto en Railway Dashboard: https://railway.app/dashboard
2. Selecciona tu servicio Django
3. Ve a **Variables** (pestaña)
4. Busca la variable `DATABASE_URL`

### Paso 2: Obtener la DATABASE_URL Correcta

#### Opción A: Usar la Variable de Referencia (RECOMENDADO)

Railway provee variables de referencia automáticas. **Elimina** la variable `DATABASE_URL` si existe y Railway la generará automáticamente cuando vincules PostgreSQL.

1. En tu servicio Django → **Settings** → **Variables**
2. Si existe una variable `DATABASE_URL` manual, **elimínala**
3. Ve a **Settings** → **Networking** 
4. Asegúrate de que PostgreSQL esté en **Linked Services** (servicios vinculados)
5. Railway automáticamente inyectará la variable `DATABASE_URL` correcta

#### Opción B: Copiar la URL Pública de PostgreSQL

Si la Opción A no funciona:

1. Ve a tu servicio **PostgreSQL** (no Django) en Railway
2. Ve a **Connect** → **Public Networking**
3. **IMPORTANTE**: Asegúrate de que "Public Networking" esté **HABILITADO** ✅
   - Si está deshabilitado, actívalo (puede tomar unos segundos)
4. Copia la **"Postgres Connection URL"** que se ve así:
   ```
   postgresql://postgres:CONTRASEÑA@región.railway.app:PUERTO/railway
   ```
5. Ve a tu servicio **Django** → **Variables**
6. Crea o actualiza la variable `DATABASE_URL` con la URL copiada

---

### Paso 3: Verificar Configuración en Railway

Asegúrate de tener estas variables configuradas en tu servicio Django:

```env
# Obligatorias
DATABASE_URL=postgresql://postgres:PASSWORD@region.railway.app:PORT/railway
DJANGO_SECRET_KEY=tu-clave-secreta-aleatoria
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=tu-app.up.railway.app,*.railway.app
PORT=8000

# Opcionales (para crear superusuario automáticamente)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=contraseña-segura
```

---

### Paso 4: Verificar que PostgreSQL esté Vinculado

1. En tu servicio Django → **Settings** → **Service**
2. Baja hasta **Linked Services**
3. Debe aparecer tu base de datos PostgreSQL
4. Si **NO** aparece:
   - Click en **+ New Service**
   - Selecciona tu PostgreSQL existente
   - O crea uno nuevo si no existe

---

### Paso 5: Redesplegar

Después de corregir la configuración:

1. **Opción A - Redeploy Manual**:
   - Railway Dashboard → tu servicio → **Deployments**
   - Click en el deployment más reciente
   - Click en **⋮** (tres puntos) → **Redeploy**

2. **Opción B - Push a Git**:
   ```bash
   git commit --allow-empty -m "trigger redeploy"
   git push origin master
   ```

---

## 🔍 Verificación Post-Despliegue

Después del redespliegue, monitorea los logs en Railway:

### ✅ Logs Esperados (Éxito)
```
Iniciando aplicación Django...
Verificando configuración...
DEBUG: 0
DATABASE_URL presente: Sí
Recolectando archivos estáticos...
X static files copied to '/app/staticfiles'
Ejecutando migraciones...
Running migrations:
  No migrations to apply.
Configuración completada. Iniciando servidor...
[INFO] Starting gunicorn
[INFO] Listening at: http://0.0.0.0:8000
```

### ❌ Logs de Error (Si persiste)
```
django.db.utils.OperationalError: could not translate host name...
```

Si ves este error después de los pasos anteriores, ve a la sección de **Troubleshooting Avanzado**.

---

## 🐛 Troubleshooting Avanzado

### Problema: El hostname sigue siendo `.railway.internal`

**Causa**: La variable `DATABASE_URL` está siendo sobreescrita en algún lugar.

**Solución**:
1. Verifica que no tengas un archivo `.env` en Railway (no debería existir)
2. En Railway Dashboard → Variables, verifica que `DATABASE_URL` tenga el formato correcto
3. Elimina cualquier referencia a `postgres.railway.internal` de las variables

### Problema: "Public Networking" no está disponible

**Causa**: Railway ha cambiado los planes o configuraciones.

**Solución alternativa - Usar Private Network**:

Si Railway fuerza el uso de networking privado, asegúrate de que:
1. Ambos servicios (Django y PostgreSQL) estén en el **mismo proyecto**
2. PostgreSQL esté en **Linked Services** del servicio Django
3. Railway generará automáticamente la variable `DATABASE_URL` con el hostname correcto

### Problema: Error de SSL/TLS

Si ves errores como:
```
SSL connection has been closed unexpectedly
```

**Solución**: Ya está configurado en `settings.py` (línea 96):
```python
ssl_require=False
```

Si el problema persiste, intenta:
```python
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        ssl_require=False,
        conn_health_checks=True,
    )
}
```

### Problema: Timeout en la conexión

**Solución**:
1. Aumenta el timeout en `railway.json`:
   ```json
   {
     "deploy": {
       "startCommand": "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 180 --max-requests 1000"
     }
   }
   ```

---

## 📋 Checklist de Verificación

- [ ] PostgreSQL tiene **Public Networking habilitado** O está en **Linked Services**
- [ ] Variable `DATABASE_URL` tiene el formato correcto (no contiene `.railway.internal`)
- [ ] Variable `DJANGO_DEBUG=0` está configurada
- [ ] Variable `DJANGO_ALLOWED_HOSTS` incluye tu dominio de Railway
- [ ] Variable `DJANGO_SECRET_KEY` está configurada (diferente a la de desarrollo)
- [ ] Ambos servicios (Django y PostgreSQL) están en el **mismo proyecto de Railway**
- [ ] Se hizo redeploy después de cambiar las variables

---

## 🆘 Si Nada Funciona

### Solución Nuclear: Recrear la Conexión a Base de Datos

**⚠️ ADVERTENCIA**: Esto no borrará datos, pero regenerará las credenciales.

1. En Railway Dashboard → tu servicio Django → **Settings**
2. En **Linked Services**, desvincula PostgreSQL
3. Espera 10 segundos
4. Vuelve a vincular PostgreSQL
5. Railway regenerará automáticamente `DATABASE_URL`
6. Redeploy

### Última Opción: Crear Nueva Base de Datos

**⚠️ ADVERTENCIA**: Esto **BORRARÁ** todos los datos.

1. Railway Dashboard → Proyecto → **+ New**
2. Selecciona **PostgreSQL**
3. Una vez creado, ve a tu servicio Django → **Settings** → **Service**
4. En **Linked Services**, agrega el nuevo PostgreSQL
5. La antigua base de datos se puede eliminar después de verificar que todo funciona

---

## 📞 Contacto con Soporte de Railway

Si el problema persiste después de todos estos pasos:

1. Ve a Railway Discord: https://discord.gg/railway
2. Canal: **#help**
3. Proporciona:
   - Logs completos del error
   - Confirmación de que PostgreSQL está vinculado
   - Confirmación de que Public Networking está habilitado (o que estás usando private network)

---

**Última actualización**: Octubre 12, 2025  
**Problema resuelto**: Error de hostname `postgres.railway.internal` no resuelve

