from typing import Any, List

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []  # type: List[Any]

    operations = [
        migrations.CreateModel(
            name="SandstormUser",
            fields=[
                (
                    "id",
                    models.CharField(
                        max_length=32,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Sandstorm User ID",
                    ),
                ),
                (
                    "handle",
                    models.CharField(max_length=200, verbose_name="handle"),
                ),
                (
                    "name",
                    models.CharField(max_length=200, verbose_name="name"),
                ),
                ("email", models.EmailField(blank=True, max_length=254)),
                (
                    "session_key",
                    models.CharField(
                        max_length=64, verbose_name="session key"
                    ),
                ),
            ],
        ),
    ]
