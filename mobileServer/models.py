from django.db import models

# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=30)
    rating = models.DecimalField(max_digits=5, decimal_places=4)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return self.name+" ("+self.lat.__str__()+","+self.lon.__str__()+")"

