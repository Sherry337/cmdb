# Generated by Django 2.1.3 on 2019-07-17 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='info',
            field=models.TextField(help_text='描述', null=True, verbose_name='描述'),
        ),
    ]