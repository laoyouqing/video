# Generated by Django 2.1.1 on 2019-07-15 05:58

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutor',
            name='detail',
            field=tinymce.models.HTMLField(help_text='导师描述', verbose_name='导师描述'),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='name',
            field=models.CharField(help_text='导师名称', max_length=50, verbose_name='导师'),
        ),
    ]
