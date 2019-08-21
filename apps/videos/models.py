from django.db import models

# Create your models here.
from tinymce.models import HTMLField

from db.base_model import BaseModel


class Video(BaseModel):
    '''视频'''
    status_choices = (
        (0, '免费'),
        (1, '付费'),
    )
    recommend_status = (
        (0, '是'),
        (1, '否'),
    )
    name = models.CharField(max_length=50, verbose_name='名称',help_text='视频名称')
    desc = models.CharField(max_length=256, verbose_name='商品描述',help_text='商品描述')
    detail = HTMLField(verbose_name='商品简介',help_text='商品简介')
    url = models.URLField(verbose_name='视频',help_text='视频url')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='视频价格',help_text='视频价格',default=0)
    number= models.IntegerField(default=0,verbose_name='人数',help_text='人数')
    status = models.SmallIntegerField(default=0, choices=status_choices, verbose_name='视频状态',help_text='视频状态')
    image = models.CharField(max_length=1000,verbose_name='视频图片',help_text='视频图片')
    is_recommend = models.SmallIntegerField(default=0,choices=recommend_status,verbose_name='是否推荐',help_text='是否推荐')
    standard_para = models.CharField(max_length=1000, verbose_name='规格参数', help_text='规格参数',null=True,blank=True)
    try_see = models.URLField(verbose_name='试看视频',help_text='试看视频url',null=True,blank=True)


    class Meta:
        db_table = 'df_video'
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class IndexGoodsBanner(BaseModel):
    '''视频轮播商品展示模型类 轮播图'''
    status_choices = (
        (0, '否'),
        (1, '是'),
    )
    video = models.ForeignKey('Video',on_delete=models.CASCADE, verbose_name='视频',help_text='视频id')
    image = models.CharField(max_length=1000, verbose_name='图片路径',help_text='图片')
    status = models.SmallIntegerField(default=0, choices=status_choices, verbose_name='是否首页轮播',help_text='是否首页轮播')

    class Meta:
        db_table = 'df_index_banner'
        verbose_name = '轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.video.name