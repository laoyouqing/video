from django.db import models

# Create your models here.
from tinymce.models import HTMLField

from db.base_model import BaseModel


class Brand(BaseModel):
    '''品牌'''

    name = models.CharField(max_length=50, verbose_name='品牌', help_text='品牌名称')
    detail = HTMLField(verbose_name='品牌描述', help_text='品牌描述')
    image = models.CharField(max_length=1000, verbose_name='图片', help_text='图片')


    class Meta:
        db_table = 'df_brand'
        verbose_name = '品牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
