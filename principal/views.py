from django.shortcuts import render

from principal.models import Product


# Create your views here.


def index(request):
    return render(request, "principal/index.html")


def services(request):
    return render(request, "principal/services.html")


def product(request):
    product = Product.objects.all()

    return render(request, "principal/product.html", {"products": product})


def product_by_category(request, category_name):
    product = Product.objects.get(category=category_name)

    return render(request, "principal/product.html", {"products": product})


def product_id(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, "principal/product_id.html", {"product": product})
