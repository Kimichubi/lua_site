from django.shortcuts import render

from principal.models import Product


# Create your views here.


def index(request):
    return render(request, "principal/index.html")


def services(request):
    return render(request, "principal/services.html")


def product(request):
    return render(request, "principal/product.html")


def product_id(request, product_id):
    return render(request, "principal/product_id.html")
