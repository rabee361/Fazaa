# Generated by Django 5.1.2 on 2025-01-01 19:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_termsprivacy_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('days', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.AlterField(
            model_name='catalog',
            name='file',
            field=models.FileField(upload_to='media/images/catalogs/', verbose_name='الملف'),
        ),
    ]
