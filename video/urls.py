"""video URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.static import serve
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
router = DefaultRouter()


from video.settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('api-auth/', include('rest_framework.urls')),
    re_path('media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    path("api-docs/", include_docs_urls("API文档")),

    path('login/', obtain_jwt_token),
    path('user/', include('apps.users.urls')),
    path('video/', include('apps.videos.urls')),
    path('cart/', include('apps.car.urls')),
    path('order/', include('apps.order.urls')),
    path('store/', include('apps.store.urls')),
    path('brand/', include('apps.brand.urls')),
    path('tutor/', include('apps.tutor.urls')),
    path('', include(router.urls)),



]
