from django import forms


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
    file_field = MultipleFileField()


class LoginForm(forms.Form):
    email = forms.EmailField(label="E-mail")
    password = forms.CharField(label="<PASSWORD>", widget=forms.PasswordInput)
