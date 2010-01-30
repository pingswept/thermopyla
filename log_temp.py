#!/usr/bin/env python

import datetime
import sqlite3
import subprocess
import time

offset = 4.0 # to account for sensor being in warm enclosure
setpoint = 20.0
heater_state = 0

con = sqlite3.connect('/root/thermostat/thermo.db')
cur = con.cursor()

p = subprocess.Popen('/usr/local/bin/gettemp', stdout=subprocess.PIPE)
(deg_c, error) = p.communicate()

# older query from before setpoint start_time was stored as integer number of minutes

# (setpoint,) = cur.execute("SELECT 'thermolog_setpoint'.'setpoint' FROM 'thermolog_setpoint' WHERE 'thermolog_setpoint'.'start_day' * 24 + 'thermolog_setpoint'.'start_time' < strftime('%w', 'now') * 24 + TIME() ORDER BY 'thermolog_setpoint'.'start_day' * 24 + 'thermolog_setpoint'.'start_time' DESC LIMIT 1;").fetchone()

(setpoint,) = cur.execute("SELECT 'thermolog_setpoint'.'setpoint' FROM 'thermolog_setpoint' WHERE 'thermolog_setpoint'.'start_time' < strftime('%w', 'now') * 24 + TIME() ORDER BY 'thermolog_setpoint'.'start_time' DESC LIMIT 1;").fetchone()

corr_temp = float(deg_c) - offset

if corr_temp < setpoint:
    heater_state = 1

cur.execute("INSERT INTO thermolog_tempreading VALUES (NULL, '%s', '%s', 'celsius', '%s', '%s')" % (datetime.datetime.utcnow(), str(corr_temp), setpoint, heater_state))
con.commit()

#print('Temp is %s' % str(corr_temp))

#if error:
#    print('Error! Error! It is: %s' % (error))

if heater_state:
    subprocess.Popen('/usr/local/bin/dio set 37 1; /usr/local/bin/ts7500ctl --redledon', shell=True)
#        print('Heat on\n')
else:
    subprocess.Popen('/usr/local/bin/dio set 37 0; /usr/local/bin/ts7500ctl --redledoff', shell=True)
#        print('Heat off\n')

cur.close()
con.close()
