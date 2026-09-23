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


class Nationality(models.Model):
    name = models.CharField("nome", max_length=120)
    code = models.CharField("código", max_length=12, unique=True)
    sovereign_state = models.CharField(
        "estado soberano",
        max_length=120,
        blank=True,
        help_text="Usado quando a nacionalidade pertence a uma nação constituinte.",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "nacionalidade"
        verbose_name_plural = "nacionalidades"

    def __str__(self):
        return self.name


class Author(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "Homem"
        FEMALE = "female", "Mulher"
        NON_BINARY = "non_binary", "Não binário"
        OTHER = "other", "Outro"
        UNKNOWN = "unknown", "Desconhecido"

    source_id = models.CharField(
        "ID de origem",
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        editable=False,
    )
    name = models.CharField("nome", max_length=200)
    gender = models.CharField(
        "gênero",
        max_length=20,
        choices=Gender.choices,
        blank=True,
    )
    nationalities = models.ManyToManyField(
        Nationality,
        related_name="authors",
        verbose_name="nacionalidades",
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "autor"
        verbose_name_plural = "autores"

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField("nome", max_length=200, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "série"
        verbose_name_plural = "séries"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField("título", max_length=300)
    original_title = models.CharField(
        "título original",
        max_length=300,
        blank=True,
    )
    authors = models.ManyToManyField(
        Author,
        related_name="books",
        verbose_name="autores",
    )
    original_language = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
        related_name="original_language_books",
        verbose_name="idioma original",
        null=True,
        blank=True,
    )
    series = models.ForeignKey(
        Series,
        on_delete=models.SET_NULL,
        related_name="books",
        verbose_name="série",
        null=True,
        blank=True,
    )
    series_position = models.CharField(
        "posição na série",
        max_length=30,
        blank=True,
        help_text="Opcional. Ex.: 1, 2, 0.5 ou Prequel.",
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "livro"
        verbose_name_plural = "livros"

    def __str__(self):
        return self.title
