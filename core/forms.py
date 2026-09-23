from django import forms

from .models import Author, Book, Language, Nationality, Series


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
    nationalities = forms.ModelMultipleChoiceField(
        queryset=Nationality.objects.all(),
        required=False,
        label="Nacionalidade(s)",
        widget=forms.SelectMultiple(
            attrs={
                "data-enhanced-multiselect": "true",
                "data-search-placeholder": "Digite para buscar uma nacionalidade...",
                "data-empty-label": "Nenhuma nacionalidade encontrada",
            }
        ),
    )

    class Meta:
        model = Author
        fields = ["name", "sort_name", "nationalities"]
        labels = {
            "name": "Nome",
            "sort_name": "Nome de ordenação",
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
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        label="Autor(es)",
        widget=forms.SelectMultiple(
            attrs={
                "data-enhanced-multiselect": "true",
                "data-search-placeholder": "Digite para buscar um autor...",
                "data-empty-label": "Nenhum autor encontrado",
            }
        ),
    )

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
            "original_language": "Idioma original",
            "series": "Série",
            "series_position": "Posição na série",
        }
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Título usado no catálogo"}),
            "original_title": forms.TextInput(attrs={"placeholder": "Opcional"}),
            "series_position": forms.TextInput(attrs={"placeholder": "Ex.: 1"}),
        }
