# Generated by Django 3.0.6 on 2020-05-18 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='book',
            name='publish_house',
            field=models.CharField(max_length=50),
        ),
    ]