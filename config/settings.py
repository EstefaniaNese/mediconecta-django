import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-secret-key")
DEBUG = os.getenv("DJANGO_DEBUG", "0") == "1"

# ALLOWED_HOSTS configuration
allowed_hosts_str = os.getenv("DJANGO_ALLOWED_HOSTS", "mediconecta-django-production.up.railway.app,*.railway.app")
ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_str.split(",") if h.strip()]

# Log configuration for debugging
print(f"[INFO] DEBUG mode: {DEBUG}")
print(f"[INFO] ALLOWED_HOSTS: {ALLOWED_HOSTS}")

# Configuración CSRF para producción
CSRF_TRUSTED_ORIGINS = [
    f"https://{host}" for host in ALLOWED_HOSTS if host and not host.startswith("localhost") and not host.startswith("127.0.0.1")
]
# Asegurar que los orígenes de Railway estén incluidos
if not DEBUG:
    CSRF_TRUSTED_ORIGINS.extend([
        "https://mediconecta-django-production.up.railway.app",
        "https://*.railway.app",
    ])
    # Configuración de cookies seguras para producción
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = False  # Railway maneja SSL, no necesitamos redirect
    # Configuración adicional de seguridad para producción
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
else:
    # En desarrollo (HTTP), las cookies no deben ser seguras
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    # local apps
    "core",
    "accounts",
    "pacientes",
    "medicos",
    "contacto",
    "citas",
    "servicios_externos",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Configuración de seguridad para producción (ya configurado arriba en modo DEBUG)

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ---------------- Database ----------------
# Configuración automática: PostgreSQL en producción (Railway), SQLite en desarrollo
if 'DATABASE_URL' in os.environ:
    # Producción: usar PostgreSQL de Railway
    database_url = os.environ.get('DATABASE_URL')
    
    # Logging para debugging (oculta la contraseña)
    if database_url:
        # Ocultar contraseña en logs
        safe_url = database_url.split('@')[1] if '@' in database_url else 'URL no disponible'
        print(f"[INFO] Conectando a base de datos: ...@{safe_url}")
        
        # Verificar si está usando hostname antiguo
        if 'railway.internal' in database_url:
            print("[WARNING] ⚠️  DATABASE_URL usa hostname .railway.internal (obsoleto)")
            print("[WARNING] Solución: Ver RAILWAY_DATABASE_FIX.md")
    
    DATABASES = {
        'default': dj_database_url.config(
            default=database_url,
            conn_max_age=600,
            ssl_require=False,  # Railway maneja SSL en el proxy
            conn_health_checks=True,  # Verificación de salud de la conexión
        )
    }
else:
    # Desarrollo: usar SQLite
    print("[INFO] Usando SQLite para desarrollo local")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Configuración para Oracle (comentada para desarrollo)
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.oracle",
#         "NAME": os.getenv("ORACLE_NAME", "xe"),
#         "USER": os.getenv("ORACLE_USER", "mediconecta"),
#         "PASSWORD": os.getenv("ORACLE_PASSWORD", "mediconecta"),
#         "HOST": os.getenv("ORACLE_HOST", "localhost"),
#         "PORT": os.getenv("ORACLE_PORT", "1521"),
#         "OPTIONS": {
#             "wallet_location": str(BASE_DIR / "oracle_wallet"),
#             "config_dir": str(BASE_DIR / "oracle_wallet"),
#         },
#     }
# }

# ---------------- Static & Media ----------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------- Auth ----------------
LOGIN_REDIRECT_URL = "core:index"
LOGOUT_REDIRECT_URL = "accounts:login"
LOGIN_URL = "accounts:login"

# ---------------- TZ/Locale ----------------
TIME_ZONE = os.getenv("DJANGO_TIME_ZONE", "UTC")
USE_TZ = True
LANGUAGE_CODE = "es-cl"

# ---------------- Django REST Framework ----------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# ---------------- JWT Configuration ----------------
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# ---------------- Logging Configuration ----------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': False,
        },
    },
}