"""
Root-level WSGI entrypoint for Vercel deployment.
Adds the 'core/' Django project directory to sys.path
so that 'core.settings' and 'core.wsgi' are importable.
"""
import sys
import os

# Insert the Django project root (core/) into path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'core'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Vercel also accepts 'app' as the entrypoint variable
app = application
