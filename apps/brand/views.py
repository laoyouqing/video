from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser

from brand.models import Brand
from brand.serializers import BrandSerializer, BrandSerializer1
from utils.paginator import GoodsPagination


class BrandView(viewsets.ReadOnlyModelViewSet):
    '''品牌'''
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    pagination_class = GoodsPagination



# 后台管理页面
class BrandAdminView(viewsets.ModelViewSet):
    '''品牌后台'''
    serializer_class = BrandSerializer1
    queryset = Brand.objects.filter(is_delete=False)
    pagination_class = GoodsPagination  # 指定自定义分页类
    permission_classes = [IsAdminUser,]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)



