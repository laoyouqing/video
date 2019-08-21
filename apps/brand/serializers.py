from rest_framework import serializers

from brand.models import Brand


class BrandSerializer(serializers.ModelSerializer):
    '''品牌'''

    class Meta:
        model = Brand
        fields = ('id','name','detail','image')



# 后台管理序列化
class BrandSerializer1(serializers.ModelSerializer):
    '''品牌'''
    create_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    update_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Brand
        fields = '__all__'

