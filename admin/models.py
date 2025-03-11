

from django.db import models

# Create your models here.

class Admin(models.Model):
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.email}, {self.password}"


