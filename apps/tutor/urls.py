from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tutor import views

router = DefaultRouter()
router.register('tutor', views.TutorView,base_name="tutor")
router.register('tutor_admin', views.TutorAdminView,base_name="tutor_admin")
router.register('tutor_tag_admin', views.TutorTagAdminView,base_name="tutor_tag_admin")

urlpatterns = [
    path('', include(router.urls)),  # Router 方式
]