from django.db import models

# Create your models here.

class Ticker(models.Model):
    text = models.CharField(max_length=200, default="Hello World!", verbose_name = "текст")
    width = models.IntegerField(verbose_name = "ширина", default=100)
    height = models.IntegerField(verbose_name = "высота", default=100)
    duration = models.IntegerField(verbose_name = "длительность", default=3)
    def __str__(self):
        return self.text