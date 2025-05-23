# Copyright (c) 2025 Miles H. (Planned Pixel Studio)
# Licensed for personal or educational use only.
# Commercial use, redistribution, or resale requires a paid license.
# Contact: miles@plannedpixel.com

"""
WSGI config for employee_database project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_database.settings')

application = get_wsgi_application()
