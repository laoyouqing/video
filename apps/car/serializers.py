from rest_framework import serializers

from videos.models import Video


class CartSerializer(serializers.Serializer):
    """
    购物车数据序列化器
    """
    video_id = serializers.IntegerField(required=True)

    def validate(self, data):
        try:
            video = Video.objects.get(id=data['video_id'])
        except Video.DoesNotExist:
            raise serializers.ValidationError('商品不存在')

        return data


class CartVideoSerializer(serializers.ModelSerializer):
    '''购物车列表'''
    class Meta:
        model = Video
        fields = ('id','image','name','price')
