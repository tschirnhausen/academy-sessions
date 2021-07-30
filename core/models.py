from django.db import models
from core.utils import token_generator

class User(models.Model):
    token = models.CharField(max_length=32, default=token_generator())

    def __str__(self):
        return self.token

class Log(models.Model):
    error = models.CharField(max_length=800)

    def __str__(self):
        return self.error
