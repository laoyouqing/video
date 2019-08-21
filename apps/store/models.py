from django.db import models

# Create your models here.
from tinymce.models import HTMLField

from db.base_model import BaseModel


class Store(BaseModel):
    '''门店'''
    name = models.CharField(max_length=50, verbose_name='名称', help_text='店铺名称')
    detail = HTMLField(verbose_name='门店简介', help_text='门店简介')
    mobile = models.CharField(max_length=11, verbose_name='手机号',help_text='手机号')
    address = models.CharField(max_length=100, verbose_name='地址', help_text='地址')
    tip = models.CharField(max_length=100, verbose_name='tip', help_text='tip')


    class Meta:
        db_table = 'df_store'
        verbose_name = '门店'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class StoreImage(BaseModel):
    '''门店图片'''
    store = models.ForeignKey('Store',on_delete=models.CASCADE, verbose_name='门店',help_text='门店id')
    image = models.CharField(max_length=1000, verbose_name='图片路径',help_text='图片')

    class Meta:
        db_table = 'df_store_image'
        verbose_name = '门店图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.store.name
