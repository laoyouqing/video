from django.urls import path, include
from rest_framework.routers import DefaultRouter

from store import views

router = DefaultRouter()
router.register('store', views.StoreView,base_name="store")
router.register('store_admin', views.StoreAdminView,base_name="store_admin")
router.register('store_image_admin', views.StoreImageAdminView,base_name="store_image_admin")

urlpatterns = [
    path('', include(router.urls)),  # Router 方式
]