# 🚨 ERROR DE DESPLIEGUE EN RAILWAY - SOLUCIÓN RÁPIDA

## El Problema
Tu aplicación no puede conectarse a PostgreSQL porque la variable `DATABASE_URL` usa un hostname obsoleto: `postgres.railway.internal`

Railway cambió su sistema de networking y este hostname ya no funciona.

---

## ✅ SOLUCIÓN RÁPIDA (5 minutos)

### Paso 1: Ve a Railway Dashboard
https://railway.app/dashboard

### Paso 2: Obtén la DATABASE_URL Correcta

**Opción A (Recomendada)**: Dejar que Railway la genere automáticamente

1. Selecciona tu **servicio Django**
2. Ve a **Variables**
3. Si existe `DATABASE_URL`, **elimínala**
4. Ve a tu **servicio PostgreSQL**
5. Ve a **Settings** → **Networking**
6. Activa **"Public Networking"** (si no está activado)
7. Vuelve a tu servicio Django
8. Ve a **Settings** → **Linked Services**
9. Asegúrate de que PostgreSQL esté vinculado
10. Railway regenerará `DATABASE_URL` automáticamente

**Opción B**: Copiar la URL manualmente

1. Ve a tu **servicio PostgreSQL**
2. Ve a **Connect**
3. Activa **"Public Networking"** si está desactivado
4. Copia la **"Postgres Connection URL"**
5. Ve a tu servicio **Django** → **Variables**
6. Actualiza `DATABASE_URL` con la URL copiada
   - Debe verse así: `postgresql://postgres:XXX@region.railway.app:PORT/railway`
   - **NO** debe contener `.railway.internal`

### Paso 3: Redeploy
- Opción 1: Railway Dashboard → Deployments → Latest → ⋮ → Redeploy
- Opción 2: `git commit --allow-empty -m "trigger redeploy" && git push`

### Paso 4: Verificar los Logs
Deberías ver:
```
✓ DATABASE_URL configuración OK (hostname moderno)
Running migrations:
  No migrations to apply.
[INFO] Starting gunicorn
```

---

## 📖 Documentación Completa

- **`RAILWAY_DATABASE_FIX.md`**: Guía completa paso a paso con capturas y troubleshooting
- **`RAILWAY_DEPLOY.md`**: Guía general de despliegue

---

## 🔍 Script de Diagnóstico

Para verificar la configuración en Railway:

```bash
railway run python scripts/check_railway_db.py
```

Este script te dirá exactamente cuál es el problema.

---

## ❓ ¿Qué Cambió?

He actualizado tu proyecto con:

1. **Detección automática** del hostname obsoleto en `settings.py`
2. **Logs mejorados** que muestran advertencias si se detecta `.railway.internal`
3. **Script de diagnóstico** para verificar la conexión
4. **Documentación completa** en `RAILWAY_DATABASE_FIX.md`

Estos cambios no afectarán tu entorno de desarrollo local (seguirá usando SQLite).

---

## 🆘 Si Aún No Funciona

1. Lee `RAILWAY_DATABASE_FIX.md` - tiene soluciones para todos los casos
2. Verifica que PostgreSQL esté **vinculado** a tu servicio Django
3. Verifica que PostgreSQL tenga **Public Networking habilitado**
4. Ejecuta el script de diagnóstico: `railway run python scripts/check_railway_db.py`

---

**Fecha**: Octubre 12, 2025  
**Problema**: Hostname `postgres.railway.internal` obsoleto  
**Solución**: Actualizar `DATABASE_URL` con hostname moderno

