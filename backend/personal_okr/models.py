from django.db import models
# from django.conf import settings


class Objective(models.Model):

    description = models.CharField(max_length=1000)
    finished_date = models.DateField()
