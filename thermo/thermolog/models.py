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
    start_day = models.IntegerField()
    start_time = models.TimeField()
    setpoint = models.FloatField()
    def __unicode__(self):
        return u'Target of %s starting at %s on day %s' % \
        (self.setpoint, self.start_time, self.start_day)

#class RecipeEntry(models.Model):
#   ingredient = models.ForeignKey(Ingredient)
#   drink = models.ForeignKey(Drink)
#   volume = models.FloatField()
#   def __unicode__(self):
#       return str(self.drink) + ' - ' + str(self.ingredient)
#   class Meta:
#       verbose_name_plural = "recipe entries"
