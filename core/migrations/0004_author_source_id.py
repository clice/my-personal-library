from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_nationality_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="source_id",
            field=models.CharField(
                blank=True,
                editable=False,
                max_length=20,
                null=True,
                unique=True,
                verbose_name="ID de origem",
            ),
        ),
    ]
