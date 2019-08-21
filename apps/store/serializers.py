from rest_framework import serializers

from store.models import Store, StoreImage


class StoreSerializer(serializers.ModelSerializer):
    '''门店'''

    class Meta:
        model = Store
        fields = ('id','name','mobile','address')


class Store1Serializer(serializers.ModelSerializer):
    '''门店'''

    class Meta:
        model = Store
        # fields = '__all__'
        exclude=('create_time','update_time','is_delete')


class StoreImageSerializer(serializers.ModelSerializer):
    '''门店图片'''

    class Meta:
        model = StoreImage
        fields = ('id','image')



class StoreImageSerializer1(serializers.ModelSerializer):
    '''门店图片'''
    create_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    update_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = StoreImage
        fields = '__all__'


# 后台管理序列化
class StoreSerializer1(serializers.ModelSerializer):
    '''门店'''
    storeimage_set=StoreImageSerializer1(many=True,read_only=True)
    class Meta:
        model = Store
        fields = '__all__'



