# Generated by Django 3.0.6 on 2020-05-18 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_auto_20200518_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.CharField(choices=[('未借出', '未借出'), ('正常借出', '正常借出'), ('续借', '续借')], default='IN_LIBRARY', max_length=11),
        ),
    ]