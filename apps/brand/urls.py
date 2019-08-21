from django.urls import path, include
from rest_framework.routers import DefaultRouter

from brand import views

router = DefaultRouter()
router.register('brand', views.BrandView,base_name="brand")
router.register('brand_admin', views.BrandAdminView,base_name="brand_admin")

urlpatterns = [
    path('', include(router.urls)),  # Router 方式
]