from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from users import views

router = DefaultRouter()
router.register('userfav', views.UserFavViewset,base_name="userfav")
router.register('areas', views.AreasViewSet, base_name='areas')

# 后台
router.register('user_admin', views.UserAdminView, base_name='useradmin')
router.register('address_admin', views.AddressAdminView, base_name='addressadmin')
router.register('area_admin', views.AreaAdminView, base_name='areaadmin')
router.register('user_fav_admin', views.UserFavAdminView, base_name='userfavadmin')


urlpatterns = [
    path('sms/', views.SMSCodeView.as_view()),
    path('exist/', views.UserIsExistView.as_view()),
    path('register/', views.UserRegister.as_view()),
    re_path('password/(?P<mobile>1[3-9]\d{9})/', views.ForgetPassword.as_view({'put':'update'})),


    path('', include(router.urls)),  # Router 方式

    path('myvideo/', views.MyVideo.as_view()),
    path('myvideo/<int:pk>/', views.MyVideo.as_view()),
    path('usercenter/', views.UserCenter.as_view()),
    path('userinfo/<int:pk>/', views.UserInfoView.as_view({'get':'retrieve','put':'update'})),
    path('set/', views.SetView.as_view()),
    path('wxoauth/', views.WxAuthView.as_view()),


    path('admin_register/', views.AdminRegister.as_view()),
]