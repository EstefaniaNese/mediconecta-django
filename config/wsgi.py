import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

try:
    application = get_wsgi_application()
except Exception as e:
    print(f"Error al inicializar Django WSGI: {e}")
    raise
