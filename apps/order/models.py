from django.db import models

# Create your models here.
from db.base_model import BaseModel
from users.models import User
from videos.models import Video


class OrderInfo(BaseModel):
    '''订单信息'''
    ORDER_STATUS_CHOICES = (
        (1, "待支付"),
        (2, "已支付"),
        (3, "已取消"),
    )
    order_id = models.CharField(max_length=64, primary_key=True, verbose_name="订单号",help_text='订单号')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="下单用户",help_text='下单用户',null=True)
    total_count = models.IntegerField(default=1, verbose_name="商品总数",help_text='商品总数')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品总金额",help_text='商品总金额')
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name="订单状态",help_text='订单状态')

    class Meta:
        db_table = "tb_order_info"
        verbose_name = '订单基本信息'
        verbose_name_plural = verbose_name


class OrderGoods(BaseModel):
    '''订单商品'''
    ORDER_STATUS_CHOICES = (
        (1, "待支付"),
        (2, "已支付"),
        (3, "已取消"),
    )
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name="订单",help_text='订单')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name="订单商品",help_text='订单商品',null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="下单用户",help_text='下单用户',null=True)
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name="订单状态",help_text='订单状态')

    class Meta:
        db_table = "tb_order_goods"
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name




