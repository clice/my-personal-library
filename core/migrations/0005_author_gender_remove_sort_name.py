from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_author_source_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[
                    ("male", "Homem"),
                    ("female", "Mulher"),
                    ("non_binary", "Não binário"),
                    ("other", "Outro"),
                    ("unknown", "Desconhecido"),
                ],
                max_length=20,
                verbose_name="gênero",
            ),
        ),
        migrations.RemoveField(
            model_name="author",
            name="sort_name",
        ),
        migrations.AlterModelOptions(
            name="author",
            options={
                "ordering": ["name"],
                "verbose_name": "autor",
                "verbose_name_plural": "autores",
            },
        ),
    ]
