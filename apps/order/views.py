import datetime
import time

from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import viewsets, status, filters
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import OrderInfo, OrderGoods
from order.serializers import OrderSerializer, Order1Serializer, OrderGoodsSerializer, OrderAdminSerializer1, \
    OrderGoodsAdminSerializer1, OrderGoodsAdminSerializer2
from order.utils import Alipay_Access
from utils.paginator import GoodsPagination
from videos.models import Video


class Order(viewsets.ModelViewSet):
    '''订单'''
    serializer_class = OrderSerializer
    lookup_field = 'order_id'
    pagination_class = GoodsPagination
    permission_classes = [IsAuthenticated]
    ordering_fields=('update_time',)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user).order_by('-update_time')

    def create(self, request, *args, **kwargs):
        ser=Order1Serializer(data=request.data)
        ser.is_valid(raise_exception=True)

        goods_ids=request.data.get('goods_ids')
        count=request.data.get('count')
        user=request.user
        total_price=0
        # 订单id
        order_id = datetime.datetime.today().strftime('%Y%m%d%H%M%S') + str(user.id)
        order = OrderInfo.objects.create(
            order_id=order_id,
            user=user,
            total_count=count,
            total_amount=total_price,
        )

        goods_ids=goods_ids.split(',')
        for goods_id in goods_ids:
            try:
                video=Video.objects.get(id=goods_id)
            except:
                OrderInfo.objects.get(order_id=order_id).delete()
                return Response({'errmsg': '商品不存在'},status=status.HTTP_400_BAD_REQUEST)

            OrderGoods.objects.create(
                order=order,
                video=video,
                user=user
            )
            total_price+=video.price
            order.total_amount=total_price
            order.save()

            redis_conn = get_redis_connection('cart')
            user = request.user
            a=redis_conn.lrem('cart_%s' % user.id, 0, goods_id)
        return Response({'order_id':order_id,'total_amount':order.total_amount})

    def list(self, request, *args, **kwargs):
        statu=request.query_params.get('status')

        if not statu:
            orders = OrderInfo.objects.filter(user=request.user, is_delete=False).order_by('-update_time')
        else:
            orders=OrderInfo.objects.filter(user=request.user,status=statu,is_delete=False).order_by('-update_time')
        orders = self.paginate_queryset(orders)
        li=[]
        for order in orders:
            dict={}
            dict['order_id']=order.order_id
            dict['total_count'] = order.total_count
            dict['total_amount'] = order.total_amount
            up_time=order.update_time
            otherStyleTime = up_time.strftime("%Y-%m-%d %H:%M:%S")
            dict['time']=otherStyleTime

            order_goods=order.ordergoods_set.all()
            ser=OrderGoodsSerializer(instance=order_goods,many=True)
            dict['videos']=ser.data
            li.append(dict)
        return self.get_paginated_response(li)

    def retrieve(self, request, order_id):
        print(order_id)

        try:
            order=OrderInfo.objects.get(order_id=order_id)
        except:
            return Response({'msg': '订单不存在'}, status=status.HTTP_400_BAD_REQUEST)
        dict={}
        cr_time = order.create_time
        up_time = order.update_time
        crStyleTime = cr_time.strftime("%Y-%m-%d %H:%M:%S")
        dict['cr_time'] = crStyleTime
        upStyleTime = up_time.strftime("%Y-%m-%d %H:%M:%S")
        dict['up_time'] = upStyleTime
        dict['order_id'] = order.order_id
        dict['total_count'] = order.total_count
        dict['total_amount'] = order.total_amount
        dict['status'] = order.status
        order_goods = order.ordergoods_set.all()
        ser = OrderGoodsSerializer(instance=order_goods, many=True)
        dict['videos'] = ser.data
        return Response(dict)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        instance.is_delete=True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        instance.status=3
        instance.save()
        return Response({'msg':'取消成功','order_id':instance.order_id},status=status.HTTP_200_OK)





class AgainBuy(RetrieveAPIView):
    '''再次购买'''
    serializer_class = OrderSerializer
    lookup_field = 'order_id'
    permission_classes = [IsAuthenticated]
    # ordering_fields = ('update_time',)
    queryset = OrderInfo.objects.all().order_by('-update_time')

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status=1
        instance.save()
        return Response({'msg':'订单已是待支付状态','order_id':instance.order_id},status=status.HTTP_200_OK)






class Pay(APIView):
    '''支付'''
    permission_classes = [IsAuthenticated]

    def get(self,request):
        order_id = request.query_params.get('order_id')
        if not order_id:
            return Response({'msg':'请输入订单号 order_id'},status=status.HTTP_400_BAD_REQUEST)
        return_url = request.query_params.get('return_url')
        if not return_url:
            return Response({'msg':'请输入支付成功回调地址 return_url'},status=status.HTTP_400_BAD_REQUEST)
        quit_url = request.query_params.get('quit_url')
        if not quit_url:
            return Response({'msg':'请输入支付中断回调地址 quit_url'},status=status.HTTP_400_BAD_REQUEST)

        instance = OrderInfo.objects.filter(order_id=order_id).first()

        if not instance:
            return Response({'msg':'没有此订单号'},status=status.HTTP_400_BAD_REQUEST)
        # 订单价格
        price = instance.total_amount
        user = instance.user
        if not user:
            return Response({'msg':'没有此用户'},status=status.HTTP_400_BAD_REQUEST)
        center_back_url = ''
        center_back_msg = ''
        expir_time = int(time.time()) + 5
        #判断该用户是否微信授权
        if user.openid:
            while not center_back_url and not center_back_msg and expir_time > int(time.time()):
                center_back_url, center_back_msg = Alipay_Access(order_id, user.openid, price, return_url, quit_url)
        else:
            return Response({'msg':'微信未授权'},status=status.HTTP_400_BAD_REQUEST)

        if center_back_url:
            return Response({'url':center_back_url},status=status.HTTP_200_OK)
        else:
            return Response(center_back_msg,status=status.HTTP_200_OK)


class OrderAdminView(viewsets.ModelViewSet):
    '''订单后台'''

    serializer_class = OrderAdminSerializer1
    queryset = OrderInfo.objects.filter(is_delete=False)
    pagination_class = GoodsPagination  # 指定自定义分页类
    permission_classes = [IsAdminUser, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('order_id','user__name')


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)



class OrderGoodsAdminView(viewsets.ModelViewSet):
    '''订单商品后台'''

    serializer_class = OrderGoodsAdminSerializer2
    queryset = OrderGoods.objects.filter(is_delete=False)
    pagination_class = GoodsPagination  # 指定自定义分页类
    permission_classes = [IsAdminUser, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('order__order_id', 'video__name')


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

