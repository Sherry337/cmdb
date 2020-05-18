from django.db import models

from assets.models import Servers
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class JumpServer(models.Model):
    RANK = (
        (1, 'root'),
        (2, 'admin'),
        (3, 'rd')
    )

    STATUS = (
        (1, '用户申请'),
        (2, '管理员审核'),
    )

    # username   = models.ForeignKey(User, verbose_name=u'用户名', related_name="user_name",null=True,help_text="用户名",on_delete=models.CASCADE)
    # ip         = models.ForeignKey(Servers, verbose_name="机器IP",related_name='servers_ip',on_delete=models.CASCADE, null=True,help_text="机器IP")
    # hostname   = models.ForeignKey(Servers, verbose_name="机器名称",related_name='servers_name',on_delete=models.CASCADE, null=True,help_text="机器名称")
    # rank       = models.CharField("用户等级",db_column='yum_cpmpang',choices=RANK,null=True,max_length=255,help_text='用户等级')
    # apply_time = models.DateTimeField(auto_now_add=True, verbose_name=u'申请时间')
    # status     = models.IntegerField(default=1, choices=STATUS, verbose_name='状态',help_text="状态")

    username = models.CharField(max_length=255, verbose_name=u'用户名', default=None, null=True, help_text="用户名")
    ip = models.CharField(max_length=255, verbose_name=u'主机ip', default=None, null=True, help_text="主机ip")
    hostname = models.CharField(max_length=255, verbose_name=u'主机名称', default=None, null=True, help_text="主机名称")
    rank = models.CharField("用户等级", db_column='yum_cpmpang', choices=RANK, null=True, max_length=255, help_text='用户等级')
    apply_time = models.DateTimeField(auto_now_add=True, verbose_name=u'申请时间')
    status = models.IntegerField(default=1, choices=STATUS, verbose_name='状态', help_text="状态")

    def __str__(self):
        return "{}[{}]".format(self.username, self.ip)

    class Meta:
        db_table = 'zto_jumpserver'