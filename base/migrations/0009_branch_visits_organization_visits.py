# Generated by Django 5.1 on 2025-03-25 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0008_alter_catalog_visits_alter_deliverycompanyurl_visits_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="branch",
            name="visits",
            field=models.IntegerField(default=0, verbose_name="الزيارات"),
        ),
        migrations.AddField(
            model_name="organization",
            name="visits",
            field=models.IntegerField(default=0, verbose_name="الزيارات"),
        ),
    ]
