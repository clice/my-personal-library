from django.urls import path

from . import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path("catalog/", views.catalog, name="catalog"),
    path("catalog/add/", views.book_create, name="book_add"),
    path("catalog/<int:pk>/edit/", views.book_update, name="book_edit"),
    path("catalog/<int:pk>/delete/", views.book_delete, name="book_delete"),

    path("series/", views.series_list, name="series"),
    path("series/add/", views.series_create, name="series_add"),
    path("series/<int:pk>/edit/", views.series_update, name="series_edit"),
    path("series/<int:pk>/delete/", views.series_delete, name="series_delete"),

    path("editions/", views.editions, name="editions"),

    path("authors/", views.authors, name="authors"),
    path("authors/add/", views.author_create, name="author_add"),
    path("authors/<int:pk>/edit/", views.author_update, name="author_edit"),
    path("authors/<int:pk>/delete/", views.author_delete, name="author_delete"),

    path("languages/", views.languages, name="languages"),
    path("languages/add/", views.language_create, name="language_add"),
    path("languages/<int:pk>/edit/", views.language_update, name="language_edit"),
    path("languages/<int:pk>/delete/", views.language_delete, name="language_delete"),
]
