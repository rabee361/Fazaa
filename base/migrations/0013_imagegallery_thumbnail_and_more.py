# Generated by Django 5.1 on 2025-04-12 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0012_reelsgallery_video_thumbnail"),
    ]

    operations = [
        migrations.AddField(
            model_name="imagegallery",
            name="thumbnail",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="media/images/thumbnails/",
                verbose_name="الصورة المصغرة",
            ),
        ),
        migrations.AlterField(
            model_name="reelsgallery",
            name="video_thumbnail",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="media/imagesthumbnails/",
                verbose_name="الصورة المصغرة",
            ),
        ),
    ]
