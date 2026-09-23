from django import forms

from .models import Author, Language


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ["name", "code"]
        labels = {
            "name": "Nome",
            "code": "Código",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ex.: Português"}),
            "code": forms.TextInput(attrs={"placeholder": "Ex.: pt"}),
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "sort_name"]
        labels = {
            "name": "Nome",
            "sort_name": "Nome de ordenação",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ex.: J. R. R. Tolkien"}),
            "sort_name": forms.TextInput(attrs={"placeholder": "Ex.: Tolkien, J. R. R."}),
        }
