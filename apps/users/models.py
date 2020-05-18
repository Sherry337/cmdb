from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


GENDER_CHOICES = (
    ('SA',"运维"),
    ('PMO',"项目经理"),
    ('DEV',"开发"),
    ('QA',"测试")
)

class User(AbstractUser):
    chinese_name = models.CharField("中文名",null=True,db_column='chinese_name',max_length=255,help_text="中文名")
    role = models.CharField("角色",db_column='role',max_length=32, default='DEV', choices=GENDER_CHOICES,help_text="角色")

    class Meta:
        verbose_name = "用户"
        ordering = ["id"]
        db_table = 'auth_user'


    def __str__(self):
        return "{}".format(self.username,)