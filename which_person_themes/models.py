from django.contrib.auth.models import User
from django.db import models

# Create your models here.

from django.db import models

class Theme(models.Model):
    name = models.CharField('お題名', max_length=255)
    major_class = models.CharField('大分類', max_length=255)
    medium_class = models.CharField('中分類', max_length=255)
    choice1 = models.TextField('選択肢1', max_length=255)
    choice2 = models.TextField('選択肢2', max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Voting(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    choice_num = models.IntegerField('選択肢番号')

class Comment(models.Model):
    user_name = models.CharField('ユーザ名', max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    choice_num = models.IntegerField('選択肢番号')
    comment = models.CharField('コメント', max_length=512)