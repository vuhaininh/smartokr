from django.db import models
from django.conf import settings


class Tag(models.Model):
    """Tag to be used for a objective"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Objective(models.Model):
    """Objective of an OKR"""
    description = models.CharField(max_length=1000)
    finished_date = models.DateField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.description


class KeyResult(models.Model):
    """Key Result of an Objective"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    objective = models.ForeignKey(
        Objective, related_name='key_results', on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    finished_date = models.DateField()

    def __str__(self):
        return self.description
