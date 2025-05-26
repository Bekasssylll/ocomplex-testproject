from django.db import models


class CitySearch(models.Model):
    city = models.CharField(max_length=100, unique=True)
    count = models.IntegerField(default=0)
    last_searched = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city} — {self.count} раз"

# Create your models here.
