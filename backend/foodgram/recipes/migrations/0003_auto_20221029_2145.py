# Generated by Django 2.2.19 on 2022-10-29 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20221025_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='recipes/images/', verbose_name='Картинка'),
        ),
    ]
