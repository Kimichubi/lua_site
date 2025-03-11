from django.db import models


# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=300)

    def __str__(self):
        return f"{self.name}, {self.price}"


class Image(models.Model):
    photo = models.ImageField(upload_to='product/images')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"{self.photo}, {self.product_id}"
