from django import forms

from .models import Author, Book, Language, Series


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
        fields = ["name", "sort_name", "nationalities"]
        labels = {
            "name": "Nome",
            "sort_name": "Nome de ordenação",
            "nationalities": "Nacionalidade(s)",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ex.: J. R. R. Tolkien"}),
            "sort_name": forms.TextInput(attrs={"placeholder": "Ex.: Tolkien, J. R. R."}),
        }


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ["name"]
        labels = {"name": "Nome"}
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ex.: Harry Potter"}),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "original_title",
            "authors",
            "original_language",
            "series",
            "series_position",
        ]
        labels = {
            "title": "Título",
            "original_title": "Título original",
            "authors": "Autor(es)",
            "original_language": "Idioma original",
            "series": "Série",
            "series_position": "Posição na série",
        }
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Título usado no catálogo"}),
            "original_title": forms.TextInput(attrs={"placeholder": "Opcional"}),
            "authors": forms.SelectMultiple(attrs={"size": 6}),
            "series_position": forms.TextInput(attrs={"placeholder": "Ex.: 1"}),
        }
