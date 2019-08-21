import json
import random

# Create your views here.
import time
import emoji
from django_redis import get_redis_connection
from rest_framework import status, mixins, viewsets, filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.versioning import QueryParameterVersioning
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from order.models import OrderInfo, OrderGoods
from order.serializers import OrderGoodsSerializer
from users.models import User, UserFav, Area, Address
from users.permission import IsOwnerOrReadOnly
from users.serializers import CodeCheckSerializer, CreateUserSerializer, ForgetPasswordSerializer, UserFavSerializer, \
    UserFav1Serializer, UserInfoSerializer, AddressSerializer, AreaSerializer, SubAreaSerializer, UserSerializer, \
    AddressSerializer1, AreaSerializer1, UserFavSerializer1, AdminRegisterSerializer, SubAreaSerializer2, \
    AddressSerializer2, UserFavSerializer2
from users.utils import WxOAuth
from utils.paginator import GoodsPagination
from utils.yunpian import YunPian
from video.settings import APIKEY, server_ip, server_port


class SMSCodeView(GenericAPIView):
    """短信验证码"""
    serializer_class = CodeCheckSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 生成短信验证码
        sms_code = "%06d" % random.randint(0, 999999)
        code={'code':sms_code}
        code=json.dumps(code)
        mobile = serializer.validated_data["mobile"]

        # 发送短信验证码
        yun_pian = YunPian()
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status["result"] == 'success':
            # 保存短信验证码与发送记录
            redis_conn = get_redis_connection('verify_codes')
            pl = redis_conn.pipeline()
            pl.setex("sms_%s" % mobile, 300, sms_code)
            pl.setex("send_flag_%s" % mobile, 60, 1)
            pl.execute()
            return Response({"mobile": mobile}, status=status.HTTP_201_CREATED)
        else:
            # 发送失败了
            return Response({"mobile": sms_status["msg"]}, status=status.HTTP_400_BAD_REQUEST)


class UserIsExistView(APIView):
    """用户名数量"""

    def get(self, request):
        mobile=request.query_params.get('mobile')
        count = User.objects.filter(mobile=mobile).count()
        data = {'mobile': mobile,'count': count}
        return Response(data)


class UserRegister(CreateAPIView):
    '''注册'''

    serializer_class = CreateUserSerializer


class ForgetPassword(mixins.UpdateModelMixin,viewsets.GenericViewSet):
    '''忘记密码，修改密码'''

    serializer_class = ForgetPasswordSerializer
    queryset = User.objects.all()
    lookup_field = 'mobile'



class UserFavViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    """
    用户收藏视图集
    """
    lookup_field = 'goods_id'
    serializer_class = UserFavSerializer
    pagination_class = GoodsPagination
    # 认证类
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 权限认证类
    # IsAuthenticated：必须登录用户；IsOwnerOrReadOnly：必须是当前登录的用户
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        # 返回当前用户的列表
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserFavSerializer
        else:
            return UserFav1Serializer


class MyVideo(ListAPIView,DestroyAPIView):
    '''我的视频'''

    pagination_class = GoodsPagination
    permission_classes = [IsAuthenticated]
    serializer_class = OrderGoodsSerializer


    def get_queryset(self):
        return OrderGoods.objects.filter(user=self.request.user,is_delete=False,status=2)


    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete=True
        instance.save()
        return Response({'msg':'删除成功'})



class UserCenter(APIView):
    '''个人中心 '''
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user=request.user
        order_count=OrderInfo.objects.filter(is_delete=False,user=user).count()
        unpay_count=OrderInfo.objects.filter(status=1,is_delete=False,user=user).count()
        suc_count=OrderInfo.objects.filter(status=2,is_delete=False,user=user).count()
        cancal_count=OrderInfo.objects.filter(status=3,is_delete=False,user=user).count()
        fav_count=UserFav.objects.filter(user=user,is_delete=False).count()
        video_count=OrderGoods.objects.filter(user=user,is_delete=False,status=2).count()

        dict={}
        name=user.name
        if name:
            name = emoji.emojize(name)
        dict['username']=name
        dict['photo']=user.photo
        dict['mobile']=user.mobile
        dict['order_count']=order_count
        dict['unpay_count']=unpay_count
        dict['suc_count']=suc_count
        dict['cancal_count']=cancal_count
        dict['fav_count']=fav_count
        dict['video_count']=video_count
        return Response(dict)


class UserInfoView(viewsets.GenericViewSet, mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    '''个人信息'''
    serializer_class = UserInfoSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]




class AreasViewSet(CacheResponseMixin,ReadOnlyModelViewSet):
    """
    行政区划信息
    """
    serializer_class = SubAreaSerializer2
    queryset = Area.objects.filter(parent_id=None)




class SetView(APIView):
    '''设置'''
    versioning_class = QueryParameterVersioning
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user=request.user
        version=request.version
        dict={}
        dict['username']=user.username
        dict['photo']=user.photo
        dict['version']=version
        return Response(dict)







# 后台管理接口

class UserAdminView(viewsets.ModelViewSet):
    '''用户后台'''
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_staff=0)
    pagination_class = GoodsPagination  # 指定自定义分页类
    permission_classes = [IsAdminUser, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','username','mobile')


class AddressAdminView(viewsets.ModelViewSet):
    '''用户地址后台'''
    serializer_class = AddressSerializer1
    queryset = Address.objects.all()
    pagination_class = GoodsPagination  # 指定自定义分页类
    permission_classes = [IsAdminUser, ]
    # filters.SearchFilter.search_description=('昵称',)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__name',)



    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return AddressSerializer1
        else:
            return AddressSerializer2



class AreaAdminView(viewsets.ModelViewSet):
    '''区域地址后台'''
    serializer_class = AreaSerializer1
    queryset = Area.objects.all()
    pagination_class = GoodsPagination  # 指定自定义分页类
    permission_classes = [IsAdminUser, ]



class UserFavAdminView(viewsets.ModelViewSet):
    '''用户收藏后台'''
    serializer_class = UserFavSerializer1
    queryset = UserFav.objects.all()
    pagination_class = GoodsPagination  # 指定自定义分页类
    permission_classes = [IsAdminUser, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__name', 'goods__name')


    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return UserFavSerializer1
        else:
            return UserFavSerializer2




class WxAuthView(APIView):
    '''微信登录用户'''

    def get(self,request):
        code = request.query_params.get('code')
        if not code:
            return Response({'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)
        oauth = WxOAuth()
        try:
            #获取授权用户access_token,openid
            access_token,openid= oauth.get_access_token(code)
        except:
            return Response({'message': '微信服务异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        try:
            user = User.objects.get(openid=openid)
            # 找到用户, 生成token
        except:
            # 判断是否是已登录的用户
            user=request.user
            if isinstance(user,User):
                user.openid=openid
                user.save()
            else:
                # 用户第一次使用wx登录
                openid,nickname,headimgurl,sex= oauth.get_user_info(access_token, openid)
                print(nickname)
                #emoji表情转换
                nickname = emoji.demojize(nickname)
                print(nickname)
                username= str(time.time()) + str(random.random())
                user=User.objects.create(openid=openid,photo=headimgurl,name=nickname,username=username,sex=int(sex)-1)

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        print(token,user.id)

        return Response({'token': token,'user_id': user.id,'username': user.name})



# 管理员注册
class AdminRegister(CreateAPIView):
    '''管理员注册'''

    serializer_class = AdminRegisterSerializer