from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Workorder(models.Model):

    STATUS = (
        (1, '待处理'),
        (2, '完成'),
    )

    work_name = models.CharField("报警名称",default=None,db_column='work_name',max_length=255,help_text="报警名称")
    content = models.CharField("报警内容",default=None,db_column='content',max_length=255,help_text="content")
    manager_user = models.ForeignKey(User, verbose_name=u'处理人', related_name="managerUser",help_text="处理人",null=True,on_delete=models.CASCADE)
    info = models.TextField(verbose_name=u'描述', null=True, help_text="描述")
    status = models.IntegerField(default=1, choices=STATUS, verbose_name='处理状态', help_text="处理状态")
    start_time = models.DateTimeField(auto_now_add=True, verbose_name=u'发生时间')
    stop_time = models.DateTimeField(auto_now=True, verbose_name=u'完成时间')


    def __str__(self):
        return "{}".format(self.work_name, )

    class Meta:
        db_table = 'zto_workorder'
        ordering = ["-id"]