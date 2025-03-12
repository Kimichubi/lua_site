from django import forms
from django.contrib.auth.forms import AuthenticationForm

from principal.models import Category


# Configuração para aceitar mais de uma imagem.
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


# Classe do Form para colocar no template HTML
class FileFieldForm(forms.Form):
    title = forms.CharField(label="Titúlo", max_length=100)
    desc = forms.CharField(label="Descrição", max_length=100)
    price = forms.IntegerField(label="Preço")
    category = forms.ModelChoiceField(label="Categoria", queryset=Category.objects.all())
    file_field = MultipleFileField()


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="E-mail", help_text="Insira seu e-mail")
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
        help_text="Insira sua senha",
        strip=False
    )
