from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from forms import FileFieldForm


# Create your views here.

class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "admin/product_register.html"  # Replace with your template.
    success_url = reverse_lazy("dashboard")  # Replace with your URL or reverse().

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        for f in files:
            print(f"Nome do arquivo: {f.name}, Tamanho: {f.size} bytes")
        return super().form_valid(form)


def index(request):
    return render(request, "admin/index.html")


def dashboard(request):
    return render(request, "admin/dashboard.html")


def product_edit(request, product_id):
    return render(request, "admin/product_edit.html")
