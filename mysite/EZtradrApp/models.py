from django.db import models

# Create your models here.
class Stock(models.Model):

    ticker = models.CharField(max_length=20)
    open = models.CharField(max_length=50)
    close = models.CharField(max_length=50)
    volume = models.IntegerField(default=0.0)
    high = models.CharField(max_length=50)
    low = models.CharField(max_length=50)
    adjClose = models.CharField(max_length=50)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.ticker

class Watch(models.Model):

    ticker = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.ticker
