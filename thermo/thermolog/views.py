from django.shortcuts import render_to_response
from thermo.thermolog.models import Setpoint, TempReading
from datetime import *
from time import *

def index(request):
    start_time = datetime.now() - timedelta(hours=4)
    data = TempReading.objects.filter(timestamp__gte=start_time)
    unix_start = mktime(start_time.timetuple())
    readings_list = ['%d000, %s, %s, %s' % (t * 60 + unix_start, row.temperature, row.setpoint, row.heater_state) \
        for (row, t) in zip(data, range(len(data)))]

    return render_to_response('index.html', {'readings_list': readings_list})

