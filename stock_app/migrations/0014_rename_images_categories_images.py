# Generated by Django 3.2.15 on 2022-10-08 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0013_auto_20221008_1205'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categories',
            old_name='Images',
            new_name='images',
        ),
    ]