# Generated by Django 5.1.2 on 2025-01-01 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_delete_report'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subscription',
        ),
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(default='media/images/users/placeholder.jpg', upload_to='media/images/users/', verbose_name='الصورة الشخصية'),
        ),
    ]