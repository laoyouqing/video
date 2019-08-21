from django.urls import path, include
from rest_framework.routers import DefaultRouter

from order import views
from order.utils import Alipay_Access, PaymentCenterRuiZ

router = DefaultRouter()
router.register('order', views.Order,base_name="order")
router.register('order_admin', views.OrderAdminView,base_name="order_admin")
router.register('order_goods_admin', views.OrderGoodsAdminView,base_name="order_goods_admin")


urlpatterns = [
    # path('sms/', views.SMSCodeView.as_view()),
    path('', include(router.urls)),  # Router 方式
    path('again_buy/<int:order_id>/', views.AgainBuy.as_view()),
    path('pay/', views.Pay.as_view()),
    path('pay_suc/', PaymentCenterRuiZ),
]
