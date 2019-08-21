from django.contrib import admin

# Register your models here.
from videos.models import IndexGoodsBanner, Video

admin.site.register(IndexGoodsBanner)
admin.site.register(Video)

