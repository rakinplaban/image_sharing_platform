# Generated by Django 3.2.15 on 2022-10-09 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0014_rename_images_categories_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
