from rest_framework import serializers

from videos.models import IndexGoodsBanner, Video


class BannerSerializer(serializers.ModelSerializer):
    '''轮播图'''

    class Meta:
        model = IndexGoodsBanner
        fields = ('video','image')



class IndexSerializer(serializers.ModelSerializer):
    '''首页'''


    class Meta:
        model = Video
        fields = ('id','image','name','desc','status','url','try_see')


class DetailSerializer(serializers.ModelSerializer):
    '''详情'''

    class Meta:
        model = Video
        fields = ('id','image','name','desc','price','url','detail','number','standard_para','try_see','status','indexgoodsbanner_set')
        depth=1





class IndexGoodsBannerSerializer1(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    update_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    '''视频图片'''
    class Meta:
        model = IndexGoodsBanner
        fields = '__all__'



# 后台
class VideoSerializer1(serializers.ModelSerializer):
    '''视频'''
    create_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    update_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    number = serializers.IntegerField(read_only=True)
    indexgoodsbanner_set = IndexGoodsBannerSerializer1(many=True,read_only=True)
    class Meta:
        model = Video
        fields = '__all__'








class UploadImageSerializer(serializers.Serializer):
    '''图片上传'''

    image=serializers.ImageField()




class UploadVideoSerializer(serializers.Serializer):
    '''视频上传'''

    video=serializers.FileField()