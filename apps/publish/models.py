from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Project(models.Model):
    project_name = models.CharField("项目名",default=None,db_column='project_name',max_length=255,help_text="项目名")
    desc         = models.TextField('项目描述', db_column='description', null=True, max_length=2550, help_text="服务描述")
    dev_user     = models.ManyToManyField(User,db_column='dev_user', verbose_name="开发人", related_name="dev_user", help_text="开发人")
    audit_user   = models.ManyToManyField(User,db_column='audit_user', verbose_name="审核人", related_name="audit_user", help_text="审核人")
    release_user = models.ManyToManyField(User,db_column='release_user', verbose_name="发布人", related_name="release_user", help_text="发布人")

    def __str__(self):
        return "{}".format(self.project_name, )

    class Meta:
        db_table = 'zto_project'


class Deploy(models.Model):
    STATUS = (
        (1, '申请'),
        (2, '审核'),
        (3, '正在发布'),
        (4, '发布完成'),
    )

    RELEASE_STATUS = (
          (1, '发布成功'),
          (2, '发布失败'),
          (3, '终止发布')
      )

    project_name = models.CharField(max_length=40, verbose_name=u'项目名称', default=None, help_text="项目名称")
    version = models.CharField(max_length=40, verbose_name=u'上线版本', default=None, help_text="上线版本")
    info = models.TextField(verbose_name=u'版本描述',null=True, help_text="版本描述")
    applicant = models.ForeignKey(User, verbose_name=u'申请人', related_name="applicant_user",help_text="申请人",on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, verbose_name=u'审核人', related_name="reviewer_user",null=True,help_text="审核人",on_delete=models.CASCADE)
    assign_to = models.ForeignKey(User, verbose_name=u'上线人',null=True, related_name="assigned_user",help_text="上线人",on_delete=models.CASCADE)
    # detail = models.TextField(verbose_name=u'更新详情')
    status = models.IntegerField(default=1, choices=STATUS, verbose_name='上线状态',help_text="上线状态")
    release_status =  models.IntegerField(choices=RELEASE_STATUS,null=True, verbose_name="发布完成状态",help_text="发布完成状态")
    console_output = models.TextField(null=True, verbose_name='上线输出结果', help_text='jenkins控制台输出的结果')
    apply_time = models.DateTimeField(auto_now_add=True, verbose_name=u'申请时间')
    deploy_time = models.DateTimeField(auto_now=True, verbose_name=u'上线完成时间')

    def __str__(self):
        return "{}".format(self.project_name, )

    class Meta:
        db_table = 'zto_deploy'
        ordering = ["-id"]