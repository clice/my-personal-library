from django.shortcuts import render


def dashboard(request):
    return render(request, "core/dashboard.html")


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
    return _placeholder(
        request,
        "Autores",
        "Pessoas e autoria",
        "Aqui ficará a organização dos autores e, futuramente, suas relações com os livros.",
    )


def languages(request):
    return _placeholder(
        request,
        "Idiomas",
        "Organização linguística",
        "Aqui ficará a estrutura de idiomas das obras e das edições.",
    )
