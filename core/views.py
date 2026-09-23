from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from .forms import AuthorForm, LanguageForm
from .models import Author, Language


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
        if _is_modal_request(request):
            return JsonResponse({"success": True})
        return redirect("authors")

    if _is_modal_request(request):
        return _modal_form_response(
            request,
            form,
            "Adicionar autor",
            "Autores",
            "Salvar autor",
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
            request,
            form,
            "Editar autor",
            "Autores",
            "Salvar alterações",
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
        html = render_to_string(
            "core/_modal_delete.html",
            {
                "item": item,
                "page_title": "Excluir autor",
                "eyebrow": "Autores",
            },
            request=request,
        )
        return JsonResponse({"html": html})

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
            request,
            form,
            "Adicionar idioma",
            "Idiomas",
            "Salvar idioma",
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
            request,
            form,
            "Editar idioma",
            "Idiomas",
            "Salvar alterações",
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
        html = render_to_string(
            "core/_modal_delete.html",
            {
                "item": item,
                "page_title": "Excluir idioma",
                "eyebrow": "Idiomas",
            },
            request=request,
        )
        return JsonResponse({"html": html})

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
