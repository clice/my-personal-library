from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AuthorForm, LanguageForm
from .models import Author, Language


def dashboard(request):
    return render(
        request,
        "core/dashboard.html",
        {
            "author_count": Author.objects.count(),
            "language_count": Language.objects.count(),
        },
    )


def _placeholder(request, title, eyebrow, description):
    return render(
        request,
        "core/placeholder.html",
        {
            "page_title": title,
            "eyebrow": eyebrow,
            "description": description,
        },
    )


def catalog(request):
    return _placeholder(
        request,
        "Catálogo",
        "Livros únicos",
        "Aqui ficará a lista de Books, sem repetir as diferentes edições da mesma obra.",
    )


def editions(request):
    return _placeholder(
        request,
        "Edições",
        "Sua coleção",
        "Aqui ficarão as edições específicas associadas aos livros do catálogo.",
    )


def authors(request):
    query = request.GET.get("q", "").strip()
    items = Author.objects.all()

    if query:
        items = items.filter(
            Q(name__icontains=query) | Q(sort_name__icontains=query)
        )

    return render(
        request,
        "core/authors.html",
        {"items": items, "query": query},
    )


def author_create(request):
    form = AuthorForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Autor adicionado com sucesso.")
        return redirect("authors")

    return render(
        request,
        "core/entity_form.html",
        {
            "form": form,
            "page_title": "Adicionar autor",
            "eyebrow": "Autores",
            "back_url": "authors",
            "submit_label": "Salvar autor",
        },
    )


def author_update(request, pk):
    item = get_object_or_404(Author, pk=pk)
    form = AuthorForm(request.POST or None, instance=item)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Autor atualizado com sucesso.")
        return redirect("authors")

    return render(
        request,
        "core/entity_form.html",
        {
            "form": form,
            "page_title": "Editar autor",
            "eyebrow": "Autores",
            "back_url": "authors",
            "submit_label": "Salvar alterações",
        },
    )


def author_delete(request, pk):
    item = get_object_or_404(Author, pk=pk)

    if request.method == "POST":
        item.delete()
        messages.success(request, "Autor excluído com sucesso.")
        return redirect("authors")

    return render(
        request,
        "core/entity_confirm_delete.html",
        {
            "item": item,
            "page_title": "Excluir autor",
            "eyebrow": "Autores",
            "back_url": "authors",
        },
    )


def languages(request):
    query = request.GET.get("q", "").strip()
    items = Language.objects.all()

    if query:
        items = items.filter(
            Q(name__icontains=query) | Q(code__icontains=query)
        )

    return render(
        request,
        "core/languages.html",
        {"items": items, "query": query},
    )


def language_create(request):
    form = LanguageForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Idioma adicionado com sucesso.")
        return redirect("languages")

    return render(
        request,
        "core/entity_form.html",
        {
            "form": form,
            "page_title": "Adicionar idioma",
            "eyebrow": "Idiomas",
            "back_url": "languages",
            "submit_label": "Salvar idioma",
        },
    )


def language_update(request, pk):
    item = get_object_or_404(Language, pk=pk)
    form = LanguageForm(request.POST or None, instance=item)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Idioma atualizado com sucesso.")
        return redirect("languages")

    return render(
        request,
        "core/entity_form.html",
        {
            "form": form,
            "page_title": "Editar idioma",
            "eyebrow": "Idiomas",
            "back_url": "languages",
            "submit_label": "Salvar alterações",
        },
    )


def language_delete(request, pk):
    item = get_object_or_404(Language, pk=pk)

    if request.method == "POST":
        item.delete()
        messages.success(request, "Idioma excluído com sucesso.")
        return redirect("languages")

    return render(
        request,
        "core/entity_confirm_delete.html",
        {
            "item": item,
            "page_title": "Excluir idioma",
            "eyebrow": "Idiomas",
            "back_url": "languages",
        },
    )
