import base64
import hashlib
import random
import string
import time

from django.shortcuts import render

# Create your views here.
from rest_framework import generics, mixins, viewsets, filters, status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from utils.paginator import GoodsPagination
from video import settings
from video.settings import MEDIA_URL, APPID, SECRET
from videos.models import IndexGoodsBanner, Video
from videos.serializers import BannerSerializer, UploadImageSerializer, IndexSerializer, DetailSerializer, \
    VideoSerializer1, IndexGoodsBannerSerializer1, UploadVideoSerializer
from videos.utils import get_jsapi_ticket, get_accesstoken


class BannerView(ListAPIView):
    serializer_class = BannerSerializer
    queryset = IndexGoodsBanner.objects.filter(status=1)



class IndexView(CacheResponseMixin,ListAPIView):
    '''首页'''

    serializer_class = IndexSerializer
    queryset = Video.objects.filter(is_recommend=0)
    pagination_class = GoodsPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)



class VideoList(CacheResponseMixin,ListAPIView):
    '''视频列表'''

    serializer_class = IndexSerializer
    pagination_class = GoodsPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        status=self.request.query_params.get('status')
        if status:
            return Video.objects.filter(status=status)
        else:
            return Video.objects.all()



class DetailView(RetrieveAPIView):
    '''详情页'''
    serializer_class = DetailSerializer
    pagination_class = GoodsPagination
    queryset = Video.objects.all()





# 后台管理页面
class VideoAdminView(viewsets.ModelViewSet):
    '''视频后台'''
    serializer_class = VideoSerializer1
    queryset = Video.objects.all()
    pagination_class = GoodsPagination  # 指定自定义分页类
    permission_classes = [IsAdminUser, ]
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    search_fields = ('name',)
    filter_fields=('status',)





class IndexGoodsBannerAdminView(viewsets.ModelViewSet):
    '''视频图片后台'''
    serializer_class = IndexGoodsBannerSerializer1
    queryset = IndexGoodsBanner.objects.all()
    pagination_class = GoodsPagination  # 指定自定义分页类
    permission_classes = [IsAdminUser, ]


    def create(self, request, *args, **kwargs):
        image = request._request.POST.get('image')
        id = request._request.POST.get('video_id')
        sta = request._request.POST.get('status')

        if not (image or id):
            return Response({'msg': '缺少image or video_id'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            video = Video.objects.get(id=id)
        except:
            return Response({'msg': '视频不存在'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if image.find(',') != -1:
                images = image.split(',')
                for image in images:
                    IndexGoodsBanner.objects.create(video=video, image=image,status=sta)
            else:
                IndexGoodsBanner.objects.create(video=video, image=image,status=sta)

        return Response({'msg': '添加成功'}, status=status.HTTP_201_CREATED)




class UploadImage(generics.GenericAPIView):
    '''图片上传'''
    serializer_class = UploadImageSerializer

    def post(self,request):
        image = request._request.POST.get('image')
        #base64解密
        image = image.split('base64,')[1]
        imagefile=base64.b64decode(image)
        now=time.time()
        fname = '%s/goods/%s.jpg' % (settings.MEDIA_ROOT, now)
        with open(fname, 'wb') as pic:
            pic.write(imagefile)
        url = 'http://' + self.request.get_host()+  MEDIA_URL + 'goods/' + str(now)+'.jpg'
        return Response(url)


class UploadVideo(generics.GenericAPIView):
    '''视频上传'''
    serializer_class = UploadVideoSerializer

    def post(self,request):
        ser=UploadVideoSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        video = request.data.get('video')
        fname = '%s/video/%s' % (settings.MEDIA_ROOT, video.name)

        with open(fname, 'wb') as pic:
            for c in video.chunks():
                pic.write(c)

        url = 'http://' + self.request.get_host()+  MEDIA_URL + 'video/' + video.name
        return Response({'url':url})



class ShowShareView(APIView):
    '''分享'''

    def get(self, request):

        nonceStr = ''.join(random.sample(string.ascii_letters, 32))
        url = 'http://' + request.get_host() + request.get_full_path()
        timestrip = int(time.time())
        ticket = get_jsapi_ticket(get_accesstoken(APPID, SECRET))
        strs = 'jsapi_ticket=%s&noncestr=%s&timestamp=%s&url=%s' % (ticket, nonceStr, timestrip, url)
        shaa1 = hashlib.sha1()
        shaa1.update(strs.encode('utf-8'))
        signature = shaa1.hexdigest()
        dict={}
        dict['appid'] = APPID
        dict['signature'] = signature
        dict['timestrip'] = timestrip
        dict['nonceStr'] = nonceStr
        dict['ticket'] = ticket

        return Response(dict)