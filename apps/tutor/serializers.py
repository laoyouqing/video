from rest_framework import serializers

from tutor.models import Tutor, Label


class TutorSerializer(serializers.ModelSerializer):
    '''导师'''

    class Meta:
        model = Tutor
        fields = ('id','name','detail','image')


class LabelSerializer(serializers.ModelSerializer):
    '''导师'''

    class Meta:
        model = Label
        fields = ('tag',)


class TutorLabelSerializer1(serializers.ModelSerializer):
    '''导师标签'''
    class Meta:
        model = Label
        fields = '__all__'

# 后台管理序列化
class TutorSerializer1(serializers.ModelSerializer):
    '''导师'''
    create_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    update_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    label_set=TutorLabelSerializer1(many=True,read_only=True)

    class Meta:
        model = Tutor
        fields = ('id','name','image','detail','label_set','create_time','update_time')
        # depth=1





