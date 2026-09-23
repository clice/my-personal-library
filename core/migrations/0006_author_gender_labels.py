from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_author_gender_remove_sort_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[
                    ("male", "Masculino"),
                    ("female", "Feminino"),
                    ("non_binary", "Não binário"),
                    ("collective", "Coletivo"),
                    ("other", "Outro"),
                    ("unknown", "Desconhecido"),
                ],
                max_length=20,
                verbose_name="gênero",
            ),
        ),
    ]
