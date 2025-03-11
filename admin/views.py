from PIL.ImageDraw import ImageDraw
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from forms import FileFieldForm
from principal.models import Product, Image


# Create your views here.

class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "admin/product_register.html"  # Replace with your template.
    success_url = reverse_lazy("dashboard")  # Replace with your URL or reverse().

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        title = form.cleaned_data["title"]
        desc = form.cleaned_data["desc"]
        price = form.cleaned_data["price"]

        product = Product()
        product.name = title
        product.desc = desc
        product.price = price
        product.save()

        for f in files:
            image = Image()
            image.photo = f
            image.product_id = product.id
            image.save()

        return super().form_valid(form)


def index(request):
    return render(request, "admin/index.html")


def dashboard(request):
    return render(request, "admin/dashboard.html")


def product_edit(request, product_id):
    product = Product.objects.get(id=product_id)

    image = Image.objects.filter(product_id=product.id)

    print(image)

    return render(request, "admin/product_edit.html")
