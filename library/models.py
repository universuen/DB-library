from django.db import models

# Create your models here.

class User(models.Model):

    username = models.CharField(max_length=20, unique=True)

    IDENTITY_CHOICES = [
        ('TEACHER', '老师'),
        ('STUDENT', '学生'),
    ]
    identity = models.CharField(
        max_length=7,
        choices=IDENTITY_CHOICES,
    )

    password = models.CharField(max_length=20)


class Book(models.Model):

    name = models.CharField(max_length=50)

    publish_house = models.CharField(max_length=50)

    release_date = models.DateField('发行日期')

    author = models.CharField(max_length=20)

    CATEGORY_CHOICES = [
        ('自然科学', '自然科学'),
        ('人文关怀', '人文关怀'),
    ]
    category = models.CharField(
        max_length=7,
        choices=CATEGORY_CHOICES,
        default='自然科学'
    )

    return_date = models.DateField('归还日期', null=True)

    STATUS_CHOICES = [
        ('未借出', '未借出'),
        ('已借出', '已借出'),
        ('续借', '续借'),
    ]
    status = models.CharField(
        max_length=11,
        choices=STATUS_CHOICES,
        default='IN_LIBRARY'
    )

    borrower = models.ForeignKey(User, related_name='books', on_delete=models.SET_NULL, null=True)


