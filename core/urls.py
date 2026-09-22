from django.urls import path

from . import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("catalog/", views.catalog, name="catalog"),
    path("editions/", views.editions, name="editions"),
    path("authors/", views.authors, name="authors"),
    path("languages/", views.languages, name="languages"),
]
