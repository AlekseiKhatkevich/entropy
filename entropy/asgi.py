"""
ASGI config for entropy project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from django.conf import settings
from django.db.backends.signals import connection_created
from django.dispatch import receiver

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'entropy.settings')


try:
    from django.core.asgi import get_asgi_application
except ImportError:
    from django.core.handlers.asgi import ASGIHandler

    def get_asgi_application():
        return ASGIHandler()

application = get_asgi_application()


@receiver(connection_created)
def setup_postgres(connection, **kwargs):
    """
    Drops statement execution after 30 seconds.
    https://hakibenita.com/9-django-tips-for-working-with-databases#custom-functions
    """
    if connection.vendor != 'postgresql':
        return None
    else:
        # Timeout statements after 30 seconds.
        with connection.cursor() as cursor:
            cursor.execute(f"SET statement_timeout TO {settings.DEFAULT_DATABASE_STATEMENT_TIMEOUT};")
