# Generated by Django 3.2.15 on 2022-10-17 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0015_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='name',
            field=models.CharField(max_length=25, unique=True),
        ),
        migrations.AlterField(
            model_name='categories',
            name='slug',
            field=models.CharField(max_length=25, unique=True),
        ),
    ]
