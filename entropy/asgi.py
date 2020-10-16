"""
ASGI config for entropy project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from configurations import importer

# IMPORTANT !!!
# Module code was changed in order to comply with django-configurations.
# In case of undebagable bugs - please try to revert to original asgi.py

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'entropy.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')


importer.install()

try:
    from django.core.asgi import get_asgi_application
except ImportError:
    from django.core.handlers.asgi import ASGIHandler

    def get_asgi_application():  
        return ASGIHandler()

application = get_asgi_application()
