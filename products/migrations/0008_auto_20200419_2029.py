# Generated by Django 3.0.5 on 2020-04-19 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20200419_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]