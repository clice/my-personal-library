from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from .forms import AuthorForm, BookForm, LanguageForm, SeriesForm
from .models import Author, Book, Language, Series


def _is_modal_request(request):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def _modal_form_response(request, form, title, eyebrow, submit_label):
    html = render_to_string(
        "core/_modal_form.html",
        {
            "form": form,
            "page_title": title,
            "eyebrow": eyebrow,
            "submit_label": submit_label,
        },
        request=request,
    )
    return JsonResponse({"html": html}, status=422 if form.errors else 200)


def _modal_delete_response(request, item, title, eyebrow):
    html = render_to_string(
        "core/_modal_delete.html",
        {
            "item": item,
            "page_title": title,
            "eyebrow": eyebrow,
        },
        request=request,
    )
    return JsonResponse({"html": html})


def dashboard(request):
    return render(
        request,
        "core/dashboard.html",
        {
            "book_count": Book.objects.count(),
            "author_count": Author.objects.count(),
            "language_count": Language.objects.count(),
        },
    )


def editions(request):
    return render(
        request,
        "core/placeholder.html",
        {
            "page_title": "Edições",
            "eyebrow": "Sua coleção",
            "description": "Aqui ficarão as edições específicas associadas aos livros do catálogo.",
        },
    )


def catalog(request):
    query = request.GET.get("q", "").strip()
    items = (
        Book.objects.select_related("original_language", "series")
        .prefetch_related("authors")
        .all()
    )

    if query:
        items = items.filter(
            Q(title__icontains=query)
            | Q(original_title__icontains=query)
            | Q(authors__name__icontains=query)
            | Q(series__name__icontains=query)
        ).distinct()

    return render(
        request,
        "core/catalog.html",
        {"items": items, "query": query},
    )


def book_create(request):
    form = BookForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Livro adicionado ao catálogo.")
        if _is_modal_request(request):
            return JsonResponse({"success": True})
        return redirect("catalog")

    if _is_modal_request(request):
        return _modal_form_response(
            request, form, "Adicionar livro", "Catálogo", "Salvar livro"
        )

    return render(
        request,
        "core/entity_form.html",
        {
            "form": form,
            "page_title": "Adicionar livro",
            "eyebrow": "Catálogo",
            "back_url": "catalog",
            "submit_label": "Salvar livro",
        },
    )


def book_update(request, pk):
    item = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=item)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Livro atualizado com sucesso.")
        if _is_modal_request(request):
            return JsonResponse({"success": True})
        return redirect("catalog")

    if _is_modal_request(request):
        return _modal_form_response(
            request, form, "Editar livro", "Catálogo", "Salvar alterações"
        )

    return render(
        request,
        "core/entity_form.html",
        {
            "form": form,
            "page_title": "Editar livro",
            "eyebrow": "Catálogo",
            "back_url": "catalog",
            "submit_label": "Salvar alterações",
        },
    )


def book_delete(request, pk):
    item = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        item.delete()
        messages.success(request, "Livro removido do catálogo.")
        if _is_modal_request(request):
            return JsonResponse({"success": True})
        return redirect("catalog")

    if _is_modal_request(request):
        return _modal_delete_response(request, item, "Excluir livro", "Catálogo")

    return render(
        request,
        "core/entity_confirm_delete.html",
        {
            "item": item,
            "page_title": "Excluir livro",
            "eyebrow": "Catálogo",
            "back_url": "catalog",
        },
    )


def series_list(request):
    query = request.GET.get("q", "").strip()
    items = Series.objects.annotate(book_count=Count("books", distinct=True))

    if query:
        items = items.filter(name__icontains=query)

    return render(
        request,
        "core/series.html",
        {"items": items, "query": query},
    )


def series_create(request):
    form = SeriesForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Série adicionada com sucesso.")
        if _is_modal_request(request):
            return JsonResponse({"success": True})
        return redirect("series")

    if _is_modal_request(request):
        return _modal_form_response(
            request, form, "Adicionar série", "Séries", "Salvar série"
        )

    return render(
        request,
        "core/entity_form.html",
        {
            "form": form,
            "page_title": "Adicionar série",
            "eyebrow": "Séries",
            "back_url": "series",
            "submit_label": "Salvar série",
        },
    )


def series_update(request, pk):
    item = get_object_or_404(Series, pk=pk)
    form = SeriesForm(request.POST or None, instance=item)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Série atualizada com sucesso.")
        if _is_modal_request(request):
            return JsonResponse({"success": True})
        return redirect("series")

    if _is_modal_request(request):
        return _modal_form_response(
            request, form, "Editar série", "Séries", "Salvar alterações"
        )

    return render(
        request,
        "core/entity_form.html",
        {
            "form": form,
            "page_title": "Editar série",
            "eyebrow": "Séries",
            "back_url": "series",
            "submit_label": "Salvar alterações",
        },
    )


def series_delete(request, pk):
    item = get_object_or_404(Series, pk=pk)

    if request.method == "POST":
        item.delete()
        messages.success(request, "Série excluída com sucesso.")
        if _is_modal_request(request):
            return JsonResponse({"success": True})
        return redirect("series")

    if _is_modal_request(request):
        return _modal_delete_response(request, item, "Excluir série", "Séries")

    return render(
        request,
        "core/entity_confirm_delete.html",
        {
            "item": item,
            "page_title": "Excluir série",
            "eyebrow": "Séries",
            "back_url": "series",
        },
    )


def authors(request):
    query = request.GET.get("q", "").strip()
    items = Author.objects.annotate(book_count=Count("books", distinct=True))

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
        if _is_modal_request(request):
            return JsonResponse({"success": True})
        return redirect("authors")

    if _is_modal_request(request):
        return _modal_form_response(
            request, form, "Adicionar autor", "Autores", "Salvar autor"
        )

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
        if _is_modal_request(request):
            return JsonResponse({"success": True})
        return redirect("authors")

    if _is_modal_request(request):
        return _modal_form_response(
            request, form, "Editar autor", "Autores", "Salvar alterações"
        )

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
        if _is_modal_request(request):
            return JsonResponse({"success": True})
        return redirect("authors")

    if _is_modal_request(request):
        return _modal_delete_response(request, item, "Excluir autor", "Autores")

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
        if _is_modal_request(request):
            return JsonResponse({"success": True})
        return redirect("languages")

    if _is_modal_request(request):
        return _modal_form_response(
            request, form, "Adicionar idioma", "Idiomas", "Salvar idioma"
        )

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
        if _is_modal_request(request):
            return JsonResponse({"success": True})
        return redirect("languages")

    if _is_modal_request(request):
        return _modal_form_response(
            request, form, "Editar idioma", "Idiomas", "Salvar alterações"
        )

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
        if _is_modal_request(request):
            return JsonResponse({"success": True})
        return redirect("languages")

    if _is_modal_request(request):
        return _modal_delete_response(request, item, "Excluir idioma", "Idiomas")

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
