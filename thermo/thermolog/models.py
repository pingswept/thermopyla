from django.db import models

class TempReading(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField('time of measurement')
    temperature = models.FloatField()
    units = models.CharField(max_length=32)
    setpoint = models.FloatField()
    heater_state = models.BooleanField()
    def __unicode__(self):
        return u'Reading of %s C from %s' % \
        (self.temperature, self.timestamp.strftime("%A, %d %B %Y %I:%M%p")) 

class Setpoint(models.Model):
    id = models.AutoField(primary_key=True)
    start_time = models.IntegerField() # in minutes of week
    setpoint = models.FloatField()
    def __unicode__(self):
        days =['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        hour_of_day = str((self.start_time % 1440) / 60)
        minute_of_hour = int((self.start_time % 1440) % 60)
        day_of_week = days[self.start_time / 1440]
        return u'Target of %s C starting at %s:%02d on %s' % \
        (self.setpoint, hour_of_day, minute_of_hour, day_of_week)
