from django.db import models


class CitySearch(models.Model):
    city = models.CharField(max_length=100)
    session_key = models.CharField(max_length=40)  # либо IP, либо session
    count = models.IntegerField(default=1)
    last_searched = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city} — {self.count} раз"

# Create your models here.
