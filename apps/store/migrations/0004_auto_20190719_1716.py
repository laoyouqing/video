# Generated by Django 2.1.1 on 2019-07-19 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20190715_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='mobile',
            field=models.CharField(help_text='手机号', max_length=11, verbose_name='手机号'),
        ),
    ]
