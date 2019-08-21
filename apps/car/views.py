from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from car.serializers import CartSerializer, CartVideoSerializer
from videos.models import Video


class CarView(GenericAPIView):
    '''购物车'''
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    queryset = Video.objects.all()

    def post(self, request):
        """
        添加购物车
        """
        ser = CartSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        video_id = ser.validated_data.get('video_id')

        # 用户已登录，在redis中保存
        redis_conn = get_redis_connection('cart')
        pl = redis_conn.pipeline()
        user=request.user
        bvideo_id = str(video_id).encode('utf-8')
        if bvideo_id in redis_conn.lrange('cart_%s' % user.id, 0, -1):
            return Response({'msg':'已加入购物车'},status=status.HTTP_400_BAD_REQUEST)

        # 记录购物车商品数量
        pl.lpush('cart_%s' % user.id, video_id)
        pl.execute()
        return Response(ser.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        redis_conn = get_redis_connection('cart')
        user = request.user
        # cart_ids=redis_conn.lrange('cart_%s' % user.id,0,-1)
        cart_ids=redis_conn.lrange('cart_%s' % user.id,0,-1)
        videos = Video.objects.filter(id__in=cart_ids)
        ser=CartVideoSerializer(instance=videos,many=True)

        return Response(ser.data)

    def delete(self,request,pk):
        redis_conn = get_redis_connection('cart')
        user = request.user
        a=redis_conn.lrem('cart_%s' % user.id, 0, pk)
        return Response({'msg':'删除成功'},status=status.HTTP_200_OK)





