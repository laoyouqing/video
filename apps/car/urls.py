from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from car import views


router = DefaultRouter()
# router.register('cart/', views.CarView)

urlpatterns = [
    path('', include(router.urls)),  # Router 方式

    path('cart/', views.CarView.as_view()),
    path('cart/<int:pk>/', views.CarView.as_view()),

]