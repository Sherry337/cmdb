from django.db import models
# from django.contrib.auth.models import User
from business.models import Products
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

SERVER_YUN_COMPANY = (
    ('aliyum','aliyun'),
    ('awsyun','awsyun'),
    ('txyun','txyun'),
)

ENV = (
    ('test','test'),
    ('prod','prod')
)

DISTRICT = {
    ("深圳",'shenzhen'),
    ("上海",'shanghai')
}

class Servers(models.Model):
    server_name  = models.CharField("服务器名称",default=None,db_column='server_name',max_length=255,help_text="服务器名称")
    out_ip       = models.CharField("外网IP",default=None,db_column='out_ip',max_length=20,help_text="外网IP")
    in_ip        = models.CharField("内网IP",db_column='in_ip',null=True,max_length=20,help_text="内网IP")
    os           = models.CharField("系统类型",db_column='os',null=True,max_length=255,help_text="系统类型")
    yun_company  = models.CharField("厂商",db_column='yum_cpmpang',choices=SERVER_YUN_COMPANY,null=True,max_length=255,help_text='厂商')
    env          = models.CharField("环境",db_column='env', choices=ENV,null=True,max_length=255,help_text="环境")
    district     = models.CharField("地区",db_column='district',choices=DISTRICT,null=True,max_length=255,help_text="地区")
    user         = models.ForeignKey(User,verbose_name="所属用户",related_name='user_servers',on_delete=models.CASCADE,null=True,help_text="所属用户")
    product      = models.ForeignKey(Products,verbose_name="所属产品",on_delete=models.CASCADE,null=True,help_text="所属产品")

    def __str__(self):
        return "{}[{}]".format(self.server_name, self.out_ip)

    class Meta:
        db_table = 'zto_servers'

class ServiceDirectorys(models.Model):
    directory   = models.CharField('服务目录', db_column='directory',default=None,max_length=255,help_text="服务目录")
    prot        = models.CharField('服务端口', db_column='port',max_length=255,null=True,help_text="服务端口")
    description = models.CharField('服务描述', db_column='description', null=True,max_length=255,help_text="服务描述")
    start_way   = models.CharField('启动方式',db_column='start_way',null=True,max_length=255,help_text='启动方式')
    server      = models.ForeignKey(Servers, verbose_name="所属机器",related_name='servers_servicedir',on_delete=models.CASCADE, null=True,help_text="所属机器")


    def __str__(self):
        return "{}[{}]".format(self.directory, self.prot)

    class Meta:
        db_table = 'zto_servicedirectorys'