from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="nationalities",
            field=django_countries.fields.CountryField(
                blank=True,
                help_text="Selecione uma ou mais nacionalidades.",
                multiple=True,
                verbose_name="nacionalidades",
            ),
        ),
        migrations.CreateModel(
            name="Series",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=200,
                        unique=True,
                        verbose_name="nome",
                    ),
                ),
            ],
            options={
                "verbose_name": "série",
                "verbose_name_plural": "séries",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=300,
                        verbose_name="título",
                    ),
                ),
                (
                    "original_title",
                    models.CharField(
                        blank=True,
                        max_length=300,
                        verbose_name="título original",
                    ),
                ),
                (
                    "series_position",
                    models.CharField(
                        blank=True,
                        help_text="Opcional. Ex.: 1, 2, 0.5 ou Prequel.",
                        max_length=30,
                        verbose_name="posição na série",
                    ),
                ),
                (
                    "original_language",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="original_language_books",
                        to="core.language",
                        verbose_name="idioma original",
                    ),
                ),
                (
                    "series",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="books",
                        to="core.series",
                        verbose_name="série",
                    ),
                ),
                (
                    "authors",
                    models.ManyToManyField(
                        related_name="books",
                        to="core.author",
                        verbose_name="autores",
                    ),
                ),
            ],
            options={
                "verbose_name": "livro",
                "verbose_name_plural": "livros",
                "ordering": ["title"],
            },
        ),
    ]
