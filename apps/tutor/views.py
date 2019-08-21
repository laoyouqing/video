from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from tutor.models import Tutor, Label
from tutor.serializers import TutorSerializer, LabelSerializer, TutorSerializer1, TutorLabelSerializer1
from utils.paginator import GoodsPagination


class TutorView(viewsets.ReadOnlyModelViewSet):
    '''导师'''
    serializer_class = TutorSerializer
    queryset = Tutor.objects.all()
    pagination_class = GoodsPagination

    def list(self, request, *args, **kwargs):
        queryset = Tutor.objects.all()
        li=[]
        page = self.paginate_queryset(queryset)
        for i in page:
            que=i.label_set.all()
            que=LabelSerializer(instance=que,many=True)
            serializer = self.get_serializer(i, many=False)
            dict={}
            dict['tutor']=serializer.data
            dict['label']=que.data
            li.append(dict)
        return self.get_paginated_response(li)


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        label = instance.label_set.all()
        label = LabelSerializer(instance=label, many=True)
        serializer = self.get_serializer(instance)
        dict = {}
        dict['tutor'] = serializer.data
        dict['label'] = label.data
        return Response(dict)



# 后台管理页面
class TutorAdminView(viewsets.ModelViewSet):
    '''导师后台'''
    serializer_class = TutorSerializer1
    queryset = Tutor.objects.all()
    pagination_class = GoodsPagination  # 指定自定义分页类
    permission_classes = [IsAdminUser, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)



class TutorTagAdminView(viewsets.ModelViewSet):
    '''导师标签后台'''
    serializer_class = TutorLabelSerializer1
    queryset = Label.objects.all()
    pagination_class = GoodsPagination  # 指定自定义分页类
    permission_classes = [IsAdminUser, ]


    def create(self, request, *args, **kwargs):
        tag = request._request.POST.get('tag')
        id = request._request.POST.get('tutor')
        labels = tag.split(',')
        if not (tag or id):
            return Response({'msg': 'tag or tutor'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            tutor = Tutor.objects.get(id=id)
        except:
            return Response({'msg': '导师不存在'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            for lable in labels:
                Label.objects.create(tag=lable, tutor=tutor)
        return Response({'msg': '添加成功'}, status=status.HTTP_201_CREATED)
