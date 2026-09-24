from django.db import models

class SensorReading(models.Model):
    bin_id = models.CharField(max_length=20)  # Add this
    distance = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
