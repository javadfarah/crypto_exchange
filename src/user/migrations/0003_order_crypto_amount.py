# Generated by Django 4.2.1 on 2023-07-18 19:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_remove_order_crypto_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="crypto_amount",
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
