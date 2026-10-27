"""WSGI config for the Lumera project."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lumera.settings')
application = get_wsgi_application()