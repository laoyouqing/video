from rest_framework import serializers

from order.models import OrderInfo, OrderGoods
from videos.models import Video
from videos.serializers import VideoSerializer1


class Order1Serializer(serializers.Serializer):
    '''订单'''

    goods_ids=serializers.CharField(required=True)
    count=serializers.IntegerField(required=True)




class OrderGoodsSerializer(serializers.ModelSerializer):
    '''订单'''

    video_id=serializers.IntegerField(source='video.id')
    name=serializers.CharField(source='video.name')
    image=serializers.CharField(source='video.image')
    desc = serializers.CharField(source='video.desc')
    price=serializers.DecimalField(source='video.price',max_digits=10, decimal_places=2)

    class Meta:
        model = OrderGoods
        fields = ('id','video_id','name','price','image','desc')



class OrderSerializer(serializers.ModelSerializer):
    '''订单'''
    class Meta:
        model = OrderInfo
        fields = '__all__'


# 后台
class OrderAdminSerializer1(serializers.ModelSerializer):
    '''订单'''
    create_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    update_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    ordergoods = serializers.SerializerMethodField()
    username=serializers.CharField(source='user.name')
    class Meta:
        model = OrderInfo
        fields = ('order_id','username','total_amount','total_count','status','ordergoods','create_time','update_time')

    def get_ordergoods(self,obj):
        video=OrderGoods.objects.filter(order=obj.order_id)
        return OrderGoodsAdminSerializer1(video,many=True).data


class OrderGoodsAdminSerializer1(serializers.ModelSerializer):
    '''订单商品'''

    class Meta:
        model = OrderGoods
        fields = ('id','video')
        depth=1



class OrderGoodsAdminSerializer2(serializers.ModelSerializer):
    '''订单商品'''

    class Meta:
        model = OrderGoods
        fields = '__all__'