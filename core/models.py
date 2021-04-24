from django.db import models
from academy.core.utils import token_generator

class User(models.Model):
    token = models.CharField(max_length=32, default=token_generator)

    def __str__(self):
        return self.token
