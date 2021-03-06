# Generated by Django 2.1.3 on 2019-05-29 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0005_auto_20190529_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deploy',
            name='applicant',
            field=models.ForeignKey(help_text='申请人', on_delete=django.db.models.deletion.CASCADE, related_name='applicant_user', to=settings.AUTH_USER_MODEL, verbose_name='申请人'),
        ),
        migrations.AlterField(
            model_name='deploy',
            name='assign_to',
            field=models.ForeignKey(help_text='上线人', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_user', to=settings.AUTH_USER_MODEL, verbose_name='上线人'),
        ),
        migrations.AlterField(
            model_name='deploy',
            name='reviewer',
            field=models.ForeignKey(help_text='审核人', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewer_user', to=settings.AUTH_USER_MODEL, verbose_name='审核人'),
        ),
    ]
