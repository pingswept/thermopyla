#!/usr/bin/env python

import datetime
import sqlite3
import subprocess
import time

offset = 4.0 # to account for sensor being in warm enclosure
hysteresis = 0.3
setpoint = 20.0
heater_state = 0

con = sqlite3.connect('/root/thermostat/thermo.db')
cur = con.cursor()

p = subprocess.Popen('/usr/local/bin/gettemp', stdout=subprocess.PIPE)
(deg_c, error) = p.communicate()

(setpoint,) = cur.execute("SELECT 'thermolog_setpoint'.'setpoint' FROM 'thermolog_setpoint' WHERE 'thermolog_setpoint'.'start_time' < strftime('%w', 'now') * 24 + TIME() ORDER BY 'thermolog_setpoint'.'start_time' DESC LIMIT 1;").fetchone()

(previous_heater_state,) = cur.execute("SELECT 'thermolog_tempreading'.'heater_state' FROM 'thermolog_tempreading' ORDER BY 'thermolog_tempreading'.'timestamp' DESC LIMIT 1;").fetchone()

corr_temp = float(deg_c) - offset

if corr_temp < setpoint - hysteresis:
    heater_state = 1
else if corr_temp > setpoint + hysteresis:
    heater_state = 0
else
    heater_state = previous_heater_state

cur.execute("INSERT INTO thermolog_tempreading VALUES (NULL, '%s', '%s', '%s', '%s')" % (datetime.datetime.utcnow(), str(corr_temp), setpoint, str(heater_state)))
con.commit()

if heater_state:
    subprocess.Popen('/usr/local/bin/dio set 37 1; /usr/local/bin/ts7500ctl --redledon', shell=True)
#        print('Heat on\n')
else:
    subprocess.Popen('/usr/local/bin/dio set 37 0; /usr/local/bin/ts7500ctl --redledoff', shell=True)
#        print('Heat off\n')

cur.close()
con.close()
