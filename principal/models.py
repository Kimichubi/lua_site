from django.db import models


# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=300)

    def __str__(self):
        return f"{self.name}, {self.price}"


class Image(models.Model):
    url = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.url}, {self.product_id}"
