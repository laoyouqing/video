from django.contrib.auth.models import AbstractUser
from django.db import models

from db.base_model import BaseModel
from videos.models import Video


class User(AbstractUser):
    """用户模型类"""
    sex_type=(
        (0,'男'),
        (1,'女')
    )
    name = models.CharField(max_length=100, verbose_name='昵称',null=True,blank=True,help_text='昵称')
    mobile = models.CharField(max_length=11, verbose_name='手机号',help_text='手机号')
    photo = models.CharField(max_length=1000,verbose_name='头像',help_text='头像')
    sex = models.SmallIntegerField(default=0, choices=sex_type, verbose_name='性别',help_text='性别')
    openid = models.CharField(max_length=64, verbose_name='openid', null=True,blank=True,help_text='openid')
    birthday = models.DateField(null=True,blank=True,verbose_name='生日',help_text='生日')



    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username






class UserFav(BaseModel):
    """
    用户收藏操作
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户",help_text='用户')
    goods = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name="视频", help_text="视频id")


    class Meta:
        db_table = 'tb_user_fav'
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")

    def __str__(self):
        return self.user.username



class Address(BaseModel):
    """
    用户地址
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户',help_text='用户')
    province = models.ForeignKey('Area', on_delete=models.PROTECT, related_name='province_addresses', verbose_name='省',help_text='省')
    city = models.ForeignKey('Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市',help_text='市')
    district = models.ForeignKey('Area', on_delete=models.PROTECT, related_name='district_addresses', verbose_name='区',help_text='区')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username



class Area(models.Model):
    """
    行政区划
    """
    name = models.CharField(max_length=20, verbose_name='名称',help_text='名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True, verbose_name='上级行政区划',help_text='上级行政区划')

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '行政区划'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name