from django.shortcuts import render
from django.core.paginator import Paginator
from principal.models import Product, Category


# Create your views here.


def index(request):
    return render(request, "principal/index.html")


def services(request):
    return render(request, "principal/services.html")


def product(request):
    product = Product.objects.all()
    if request.method == "POST":
        name_to_search = request.POST.get("search", "").strip()

        product = product.filter(name__icontains=name_to_search)
        print(product)

    paginator = Paginator(product, 10)

    page_number = request.GET.get("page")

    if page_number == 0:
        page_number = 1

    page_obj = paginator.get_page(page_number)
    return render(request, "principal/product.html", {"page_obj": page_obj})


def product_by_category(request, product_category):
    category = Category.objects.get(name=product_category)
    product = Product.objects.filter(category_id=category.id)

    paginator = Paginator(product, 10)
    page_number = request.GET.get("page")
    if page_number == 0:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    return render(request, "principal/product.html", {"page_obj": page_obj})


def product_id(request, product_id):
    product = Product.objects.get(id=product_id)
    related_products = Product.objects.filter(category_id=product.category_id)[:3]
    return render(request, "principal/product_id.html", {"product": product, "related_products": related_products})
