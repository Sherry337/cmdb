# Generated by Django 2.1.3 on 2019-04-29 02:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Servers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_name', models.CharField(db_column='server_name', default=None, help_text='服务器名称', max_length=255, verbose_name='服务器名称')),
                ('out_ip', models.CharField(db_column='out_ip', default=None, help_text='外网IP', max_length=20, verbose_name='外网IP')),
                ('in_ip', models.CharField(db_column='in_ip', help_text='内网IP', max_length=20, null=True, verbose_name='内网IP')),
                ('os', models.CharField(db_column='os', help_text='系统类型', max_length=255, null=True, verbose_name='系统类型')),
                ('yun_company', models.CharField(choices=[('aliyum', 'aliyun'), ('awsyun', 'awsyun'), ('txyun', 'txyun')], db_column='yum_cpmpang', help_text='厂商', max_length=255, null=True, verbose_name='厂商')),
                ('env', models.CharField(choices=[('test', 'test'), ('prod', 'prod')], db_column='env', help_text='环境', max_length=255, null=True, verbose_name='环境')),
                ('district', models.CharField(choices=[('上海', 'shanghai'), ('深圳', 'shenzhen')], db_column='district', help_text='地区', max_length=255, null=True, verbose_name='地区')),
            ],
            options={
                'db_table': 'zto_servers',
            },
        ),
        migrations.CreateModel(
            name='ServiceDirectorys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('directory', models.CharField(db_column='directory', default=None, help_text='服务目录', max_length=255, verbose_name='服务目录')),
                ('prot', models.CharField(db_column='port', help_text='服务端口', max_length=255, null=True, verbose_name='服务端口')),
                ('description', models.CharField(db_column='description', help_text='服务描述', max_length=255, null=True, verbose_name='服务描述')),
                ('start_way', models.CharField(db_column='start_way', help_text='启动方式', max_length=255, null=True, verbose_name='启动方式')),
                ('server', models.ForeignKey(help_text='所属机器', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='servers_servicedir', to='assets.Servers', verbose_name='所属机器')),
            ],
            options={
                'db_table': 'zto_servicedirectorys',
            },
        ),
    ]
