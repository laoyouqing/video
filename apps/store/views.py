from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from store.models import Store, StoreImage
from store.serializers import StoreSerializer, Store1Serializer, StoreImageSerializer, StoreSerializer1, \
    StoreImageSerializer1
from utils.paginator import GoodsPagination


class StoreView(viewsets.ReadOnlyModelViewSet):
    '''门店'''
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    pagination_class = GoodsPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return StoreSerializer
        else:
            return Store1Serializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        image=instance.storeimage_set.all()
        image=StoreImageSerializer(instance=image,many=True)
        serializer = self.get_serializer(instance)
        dict={}
        dict['store']=serializer.data
        dict['image']=image.data

        return Response(dict)



# 后台管理页面
class StoreAdminView(viewsets.ModelViewSet):
    '''门店后台'''
    serializer_class = StoreSerializer1
    queryset = Store.objects.all()
    pagination_class = GoodsPagination  # 指定自定义分页类
    permission_classes = [IsAdminUser, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)



class StoreImageAdminView(viewsets.ModelViewSet):
    '''门店图片后台'''
    serializer_class = StoreImageSerializer1
    queryset = StoreImage.objects.all()
    pagination_class = GoodsPagination  # 指定自定义分页类
    permission_classes = [IsAdminUser, ]


    def create(self, request, *args, **kwargs):
        image = request._request.POST.get('image')
        id = request._request.POST.get('store')

        if not (image or id):
            return Response({'msg': '缺少image or store'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            store = Store.objects.get(id=id)
        except:
            return Response({'msg': '门店不存在'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if image.find(',') != -1:
                images = image.split(',')
                for image in images:
                    StoreImage.objects.create(store=store, image=image)
            else:
                StoreImage.objects.create(store=store, image=image)

        return Response({'msg': '添加成功'}, status=status.HTTP_201_CREATED)





