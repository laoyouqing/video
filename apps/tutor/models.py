from django.db import models

# Create your models here.
from tinymce.models import HTMLField

from db.base_model import BaseModel


class Tutor(BaseModel):
    '''导师'''

    name = models.CharField(max_length=50, verbose_name='导师', help_text='导师名称')
    detail = HTMLField(verbose_name='导师描述', help_text='导师描述')
    image = models.CharField(max_length=1000, verbose_name='图片', help_text='图片')

    class Meta:
        db_table = 'tb_tutor'
        verbose_name = '导师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class Label(BaseModel):
    '''标签'''
    tag = models.CharField(max_length=50, verbose_name='标签', help_text='标签')
    tutor=models.ForeignKey('Tutor',on_delete=models.CASCADE,verbose_name='导师',help_text='导师id')


    class Meta:
        db_table = 'tb_label'
        verbose_name = '导师标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tutor.name
