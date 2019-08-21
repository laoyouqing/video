import re

import emoji
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_jwt.settings import api_settings

from order.models import OrderGoods, OrderInfo
from users.models import User, UserFav, Address, Area

# 手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"

class CodeCheckSerializer(serializers.Serializer):
    """
    注册手机验证校验序列化器
    """
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """自定义验证手机号码"""

        # 是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        # 判断是否在60s内
        redis_conn = get_redis_connection('verify_codes')
        send_flag = redis_conn.get("send_flag_%s" % mobile)
        if send_flag:
            raise serializers.ValidationError('请求次数过于频繁')
        return mobile


class CreateUserSerializer(serializers.ModelSerializer):
    '''注册'''
    password = serializers.CharField(label='密码', write_only=True)
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    username = serializers.CharField(label='用户名',read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username','mobile', 'password', 'password2', 'sms_code')

    def validate_mobile(self, value):
        """验证手机号"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def validate(self, data):
        # 判断两次密码
        if data['password'] != data['password2']:
            raise serializers.ValidationError('两次密码不一致')

        # 判断短信验证码
        redis_conn = get_redis_connection('verify_codes')
        mobile = data['mobile']
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        if real_sms_code is None:
            raise serializers.ValidationError('无效的短信验证码')
        if data['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError('短信验证码错误')
        return data

    def create(self, validated_data):
        """
        创建用户
        """
        # 移除数据库模型类中不存在的属性
        del validated_data['password2']
        del validated_data['sms_code']
        validated_data['username']=validated_data['mobile']

        user = super(CreateUserSerializer,self).create(validated_data)

        # 调用django的认证系统加密密码
        user.set_password(validated_data['password'])
        user.save()

        # 补充生成记录登录状态的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token

        return user



class ForgetPasswordSerializer(serializers.ModelSerializer):
    '''忘记密码,修改密码'''
    password = serializers.CharField(label='密码', write_only=True)
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    username = serializers.CharField(label='用户名', read_only=True)


    class Meta:
        model = User
        fields = ('id', 'username','mobile', 'password', 'password2', 'sms_code')

    def validate_mobile(self, value):
        """验证手机号"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def validate(self, data):
        # 判断两次密码
        if data['password'] != data['password2']:
            raise serializers.ValidationError('两次密码不一致')

        redis_conn = get_redis_connection('verify_codes')
        mobile = data['mobile']
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        if real_sms_code is None:
            raise serializers.ValidationError('无效的短信验证码')
        if data['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError('短信验证码错误')
        return data

    def update(self, instance, validated_data):
        user=User.objects.get(mobile=validated_data['mobile'])

        # 调用django的认证系统加密密码
        user.set_password(validated_data['password'])
        user.save()

        # 补充生成记录登录状态的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token

        return instance



class UserFavSerializer(serializers.ModelSerializer):
    # 获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )


    class Meta:
        # validate实现唯一联合，一个商品只能收藏一次
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                # message的信息可以自定义
                message="已经收藏"
            )
        ]
        model = UserFav
        fields = ("user", "goods")


class UserFav1Serializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    name=serializers.CharField(source='goods.name',read_only=True)
    goods_id=serializers.CharField(source='goods.id',read_only=True)
    desc=serializers.CharField(source='goods.desc')
    image=serializers.CharField(source='goods.image')
    status=serializers.CharField(source='goods.status')
    class Meta:
        # validate实现唯一联合，一个商品只能收藏一次
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                # message的信息可以自定义
                message="已经收藏"
            )
        ]
        model = UserFav
        fields = ("user", "name",'goods_id','desc','image','status')



class UserInfoSerializer(serializers.ModelSerializer):
    '''个人信息'''
    address = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ("name", "mobile", 'birthday', 'sex','photo','address')

    def get_address(self, obj):
        address=Address.objects.filter(user=obj.id)
        return AddressSerializer(address,many=True).data

    def to_representation(self, instance):
        instance = super(UserInfoSerializer, self).to_representation(instance)
        if instance['name']:
            instance['name']= emoji.emojize(instance['name'])
        return instance




class AddressSerializer(serializers.ModelSerializer):
    '''个人地址'''

    class Meta:
        model = Address
        fields = ("province", "city", 'district')




class AreaSerializer(serializers.ModelSerializer):
    """
    行政区划信息序列化器
    """
    class Meta:
        model = Area
        fields = ('id', 'name')


class SubAreaSerializer(serializers.ModelSerializer):
    """
    子行政区划信息序列化器
    """
    subs = AreaSerializer(many=True, read_only=True)
    class Meta:
        model = Area
        fields = ('id', 'name', 'subs')


class SubAreaSerializer2(serializers.ModelSerializer):
    """
    子行政区划信息序列化器
    """
    subs = SubAreaSerializer(many=True, read_only=True)
    class Meta:
        model = Area
        fields = ('id', 'name', 'subs')


# 后台管理序列化

class UserSerializer(serializers.ModelSerializer):
    '''用户'''
    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        instance = super(UserSerializer, self).to_representation(instance)
        if instance['name']:
            instance['name'] = emoji.emojize(instance['name'])
        return instance


class AddressSerializer1(serializers.ModelSerializer):
    '''用户地址'''
    class Meta:
        model = Address
        fields = '__all__'

class AddressSerializer2(serializers.ModelSerializer):
    '''用户地址'''
    class Meta:
        model = Address
        fields = '__all__'
        depth=1


class AreaSerializer1(serializers.ModelSerializer):
    '''区域地址'''
    class Meta:
        model = Area
        fields = '__all__'


class UserFavSerializer1(serializers.ModelSerializer):
    '''用户收藏'''
    create_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    update_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = UserFav
        fields = '__all__'


class UserFavSerializer2(serializers.ModelSerializer):
    '''用户收藏'''
    create_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    update_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = UserFav
        fields = '__all__'
        depth=1




class AdminRegisterSerializer(serializers.ModelSerializer):
    '''注册管理员'''
    password = serializers.CharField(label='密码', write_only=True)
    password2 = serializers.CharField(label='确认密码', write_only=True)
    username = serializers.CharField(label='用户名')

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2')

    def validate(self, data):
        # 判断两次密码
        if data['password'] != data['password2']:
            raise serializers.ValidationError('两次密码不一致')
        return data
    def create(self, validated_data):
        """
        创建管理员
        """
        # 移除数据库模型类中不存在的属性
        del validated_data['password2']
        validated_data['is_superuser']=1
        validated_data['is_staff']=1

        user = super(AdminRegisterSerializer,self).create(validated_data)

        # 调用django的认证系统加密密码
        user.set_password(validated_data['password'])
        user.save()

        # 补充生成记录登录状态的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        return user



class OrderGoodsSerializer(serializers.ModelSerializer):
    '''订单-我的视频'''

    id=serializers.IntegerField(source='video.id')
    name=serializers.CharField(source='video.name')
    image=serializers.CharField(source='video.image')
    desc = serializers.CharField(source='video.desc')
    price=serializers.DecimalField(source='video.price',max_digits=10, decimal_places=2)

    class Meta:
        model = OrderGoods
        fields = ('id','name','price','image','desc')