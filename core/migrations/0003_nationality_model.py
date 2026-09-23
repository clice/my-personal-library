from django.db import migrations, models
from django_countries import countries


SPECIAL_NATIONALITIES = [
    ("GB-ENG", "Inglaterra", "Reino Unido"),
    ("GB-SCT", "Escócia", "Reino Unido"),
    ("GB-WLS", "País de Gales", "Reino Unido"),
    ("GB-NIR", "Irlanda do Norte", "Reino Unido"),
]


def seed_and_copy_nationalities(apps, schema_editor):
    Author = apps.get_model("core", "Author")
    Nationality = apps.get_model("core", "Nationality")

    for code, name in countries:
        Nationality.objects.get_or_create(
            code=code,
            defaults={"name": str(name), "sovereign_state": ""},
        )

    for code, name, sovereign_state in SPECIAL_NATIONALITIES:
        Nationality.objects.update_or_create(
            code=code,
            defaults={
                "name": name,
                "sovereign_state": sovereign_state,
            },
        )

    for author in Author.objects.all():
        raw = author.nationalities
        if not raw:
            continue

        if isinstance(raw, str):
            codes = [part.strip() for part in raw.split(",") if part.strip()]
        elif hasattr(raw, "code"):
            codes = [raw.code]
        else:
            codes = []
            try:
                for value in raw:
                    codes.append(getattr(value, "code", str(value)))
            except TypeError:
                codes = [str(raw)]

        for code in codes:
            nationality = Nationality.objects.filter(code=code).first()
            if nationality:
                author.nationalities_new.add(nationality)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_author_nationalities_series_book"),
    ]

    operations = [
        migrations.CreateModel(
            name="Nationality",
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
                        max_length=120,
                        verbose_name="nome",
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        max_length=12,
                        unique=True,
                        verbose_name="código",
                    ),
                ),
                (
                    "sovereign_state",
                    models.CharField(
                        blank=True,
                        help_text="Usado quando a nacionalidade pertence a uma nação constituinte.",
                        max_length=120,
                        verbose_name="estado soberano",
                    ),
                ),
            ],
            options={
                "verbose_name": "nacionalidade",
                "verbose_name_plural": "nacionalidades",
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="author",
            name="nationalities_new",
            field=models.ManyToManyField(
                blank=True,
                related_name="authors_new",
                to="core.nationality",
                verbose_name="nacionalidades",
            ),
        ),
        migrations.RunPython(
            seed_and_copy_nationalities,
            migrations.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name="author",
            name="nationalities",
        ),
        migrations.RenameField(
            model_name="author",
            old_name="nationalities_new",
            new_name="nationalities",
        ),
        migrations.AlterField(
            model_name="author",
            name="nationalities",
            field=models.ManyToManyField(
                blank=True,
                related_name="authors",
                to="core.nationality",
                verbose_name="nacionalidades",
            ),
        ),
    ]
