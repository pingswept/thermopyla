import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'thermo.settings'

sys.path.append('/root/thermostat')
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
