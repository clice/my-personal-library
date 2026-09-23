from django.db import models


class Language(models.Model):
    name = models.CharField("nome", max_length=100, unique=True)
    code = models.CharField(
        "código",
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        help_text="Código curto, como pt, en ou fr.",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "idioma"
        verbose_name_plural = "idiomas"

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField("nome", max_length=200)
    sort_name = models.CharField(
        "nome de ordenação",
        max_length=200,
        blank=True,
        help_text="Opcional. Ex.: Tolkien, J. R. R.",
    )

    class Meta:
        ordering = ["sort_name", "name"]
        verbose_name = "autor"
        verbose_name_plural = "autores"

    def __str__(self):
        return self.name
