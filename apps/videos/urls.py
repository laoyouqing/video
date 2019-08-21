from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from videos import views
router = DefaultRouter()
router.register('video_admin', views.VideoAdminView,base_name="video_admin")
router.register('video_image_admin', views.IndexGoodsBannerAdminView,base_name="video_image_admin")



urlpatterns = [
    path('banner/', views.BannerView.as_view()),
    path('index/', views.IndexView.as_view()),
    path('list/', views.VideoList.as_view()),
    path('detail/<int:pk>/', views.DetailView.as_view()),
    path('uploadimage/',views.UploadImage.as_view()),
    path('uploadvideo/',views.UploadVideo.as_view()),
    path('wxshare/',views.ShowShareView.as_view()),

    path('', include(router.urls)),  # Router 方式
]