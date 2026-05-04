from django.db import models


class AirplaneType(models.Model):
    name = models.CharField(max_length=64, unique=True)
