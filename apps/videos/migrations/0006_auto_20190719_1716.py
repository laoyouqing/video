# Generated by Django 2.1.1 on 2019-07-19 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0005_remove_indexgoodsbanner_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='standard_para',
            field=models.CharField(blank=True, help_text='规格参数', max_length=100, null=True, verbose_name='规格参数'),
        ),
        migrations.AlterField(
            model_name='video',
            name='is_recommend',
            field=models.SmallIntegerField(choices=[(0, '是'), (1, '否')], default=0, help_text='是否推荐', verbose_name='是否推荐'),
        ),
        migrations.AlterField(
            model_name='video',
            name='number',
            field=models.IntegerField(default=0, help_text='人数', verbose_name='人数'),
        ),
        migrations.AlterField(
            model_name='video',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '免费'), (1, '付费')], default=0, help_text='视频状态', verbose_name='视频状态'),
        ),
    ]
