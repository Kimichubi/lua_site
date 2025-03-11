from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import authenticate, login
from admin.models import Admin
from forms import FileFieldForm, LoginForm
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
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            if email and password is not None:
                admin = Admin.objects.get(email=email)
                if admin.check_password(password):
                    return HttpResponseRedirect(reverse_lazy("dashboard"))
                else:
                    print("Invalid email or password")
            else:
                print("Invalid email or password")
    else:
        form = LoginForm()
    return render(request, "admin/index.html", {"form": form})


def dashboard(request):
    return render(request, "admin/dashboard.html")


def product_edit(request, product_id):
    product = Product.objects.get(id=product_id)

    image = Image.objects.filter(product_id=product.id)

    print(image)

    return render(request, "admin/product_edit.html")

# def create_admin(request):
#     admin = Admin(email=)
#     admin.set_password()  # Criptografa a senha
#     admin.save()
#     return HttpResponse("Criado com sucesso!")
