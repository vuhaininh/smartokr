from django.db import models


class Objective(models.Model):
    description = models.CharField(max_length=1000)
    finished_date = models.DateField()
