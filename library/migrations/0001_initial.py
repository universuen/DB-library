# Generated by Django 3.0.6 on 2020-05-18 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('identity', models.CharField(choices=[('TEACHER', '老师'), ('STUDENT', '学生')], max_length=7)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('publish_house', models.CharField(max_length=20)),
                ('release_data', models.DateField(verbose_name='发行日期')),
                ('author', models.CharField(max_length=20)),
                ('category', models.CharField(choices=[('SCIENCE', '自然科学'), ('ART', '人文关怀')], max_length=7)),
                ('return_data', models.DateField(verbose_name='归还日期')),
                ('status', models.CharField(choices=[('IN_LIBRARY', '未借出'), ('NORMAL_LENT', '正常借出'), ('RENEW', '续借'), ('OVERDUE', '逾期未还')], max_length=11)),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='library.User')),
            ],
        ),
    ]
