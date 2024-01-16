"""
WSGI config for my_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from static_ranges import Ranges
from dj_static import Cling, MediaCling
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')

# application = get_wsgi_application()
application = Ranges(Cling(MediaCling(get_wsgi_application())))
