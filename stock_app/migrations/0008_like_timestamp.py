# Generated by Django 3.2.15 on 2022-09-29 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0007_alter_images_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]