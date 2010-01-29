from django.shortcuts import render_to_response
from thermo.thermolog.models import Setpoint, TempReading
from datetime import *

def index(request):
    recent_temps_list = TempReading.objects.filter(timestamp__gte=datetime.now() - timedelta(hours=1))
    return render_to_response('index.html', {'recent_temps_list': recent_temps_list})

