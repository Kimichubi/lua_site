from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


# Create your models here.

class Admin(models.Model):
    email = models.EmailField(max_length=30, unique=True)
    password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        # Criptografa a senha antes de armazená-la
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        # Verifica se a senha está correta

        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.email}, {self.password}"
