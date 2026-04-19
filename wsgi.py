"""
Root-level WSGI entrypoint for Vercel deployment.
Adds the 'core/' Django project directory to sys.path
so that 'core.settings' and 'core.wsgi' are importable.
Auto-runs migrations on cold start for Vercel's ephemeral SQLite.
"""
import sys
import os

# Insert the Django project root (core/) into path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'core'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

from django.core.wsgi import get_wsgi_application

# Initialise Django (calls django.setup() internally)
application = get_wsgi_application()

# Auto-run migrations on every cold start.
# On Vercel the DB lives in /tmp so it resets between cold starts;
# running migrate ensures tables always exist.
from django.core.management import call_command
try:
    call_command('migrate', '--run-syncdb', verbosity=0)
except Exception as exc:
    print(f"[wsgi] migrate warning: {exc}")

# Vercel also accepts 'app' as the entrypoint variable
app = application
