from django.db import models


class Item(models.Model):
    name = models.CharField()
    description = models.CharField()
    price = models.IntegerField()
