# Generated by Django 5.1.2 on 2025-01-05 20:10

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branch',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='branch',
            name='long',
        ),
        migrations.AddField(
            model_name='branch',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(default='POINT(0.0 0.0)', srid=4326, verbose_name='الموقع'),
            preserve_default=True,
        ),
    ]