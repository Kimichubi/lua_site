from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import authenticate, login
from admin.models import Admin
from forms import FileFieldForm, LoginForm
from principal.models import Product, Image, Category
from decimal import Decimal
from django.contrib import messages

from utils import clean_orphaned_images


# Create your views here.

# Form Register
class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "admin/product_register.html"  # Replace with your template.
    success_url = reverse_lazy("dashboard")  # Replace with your URL or reverse().

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        title = form.cleaned_data["title"]
        desc = form.cleaned_data["desc"]
        price = form.cleaned_data["price"]
        category = form.cleaned_data["category"]
        category = Category.objects.get(name=category)

        product = Product()
        product.name = title
        product.description = desc
        product.price = price
        product.category_id = category.id
        product.save()

        for f in files:
            image = Image()
            image.photo = f
            image.product_id = product.id
            image.save()

        return super().form_valid(form)


# Form Login
def index(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy("dashboard"))

            # Mensagem genérica para evitar enumeração de usuários
            form.add_error(None, "Credenciais inválidas")
        else:
            print(form.errors)

    else:
        form = LoginForm()

    return render(request, "admin/index.html", {"form": form})


# Log
@login_required
def dashboard(request):
    cleaned_count = clean_orphaned_images()

    if cleaned_count > 0:
        messages.warning(request, f"{cleaned_count} imagens inválidas foram removidas do banco de dados")
    products = Product.objects.all().prefetch_related('images')
    paginator = Paginator(products, 10)

    page_number = request.GET.get("page")

    if page_number == 0:
        page_number = 1

    page_obj = paginator.get_page(page_number)
    return render(request, "admin/dashboard.html", {"page_obj": page_obj})


@login_required
def product_edit(request, product_id):
    product = Product.objects.get(id=product_id)
    categories = Category.objects.all()
    if request.method == "POST":

        try:
            # Atualiza os campos básicos
            product.name = request.POST.get("title", "").strip()
            product.description = request.POST.get("desc", "").strip()
            category_name = request.POST.get("category", "").strip()
            category = Category.objects.get(name=category_name)
            product.category_id = category.id
            print(product.description)

            # Converte o preço para Decimal
            price_str = request.POST.get("price", "0").strip()
            try:
                product.price = Decimal(price_str)
            except (ValueError, TypeError):
                raise ValidationError("Preço inválido. Use números decimais.")

            # Salva o produto
            product.save()

            # Lida com a exclusão de imagens
            delete_images = request.POST.getlist("delete_images")
            if delete_images:
                Image.objects.filter(id__in=delete_images).delete()

            # Lida com o upload de novas imagens
            new_images = request.FILES.getlist("new_images")
            for image_file in new_images:
                Image.objects.create(product=product, photo=image_file)

            # Mensagem de sucesso
            messages.success(request, "Produto atualizado com sucesso!")
            return redirect('dashboard')

        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao atualizar o produto: {str(e)}")

        # Renderiza o template de edição
    images = Image.objects.filter(product=product)
    return render(request, "admin/product_edit.html", {
        "product": product,
        "images": images,
        "categories": categories,
    })


# def create_admin(request):
#     super_usuario = Admin.objects.create_superuser(
#         email=,
#         password='
#     )
#     return HttpResponse("Criado com sucesso!")
@login_required
def delete_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product_name = product.name
        product.delete()
        messages.success(request, f'Produto "{product_name}" excluído com sucesso!')
        return redirect('dashboard')
    else:
        return redirect('dashboard')
