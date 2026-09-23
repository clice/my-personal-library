from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
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
                ("name", models.CharField(max_length=200, verbose_name="nome")),
                (
                    "sort_name",
                    models.CharField(
                        blank=True,
                        help_text="Opcional. Ex.: Tolkien, J. R. R.",
                        max_length=200,
                        verbose_name="nome de ordenação",
                    ),
                ),
            ],
            options={
                "verbose_name": "autor",
                "verbose_name_plural": "autores",
                "ordering": ["sort_name", "name"],
            },
        ),
        migrations.CreateModel(
            name="Language",
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
                        max_length=100,
                        unique=True,
                        verbose_name="nome",
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        blank=True,
                        help_text="Código curto, como pt, en ou fr.",
                        max_length=10,
                        null=True,
                        unique=True,
                        verbose_name="código",
                    ),
                ),
            ],
            options={
                "verbose_name": "idioma",
                "verbose_name_plural": "idiomas",
                "ordering": ["name"],
            },
        ),
    ]
