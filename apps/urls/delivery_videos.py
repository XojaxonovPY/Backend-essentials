from django.urls import path

from apps.views import FoodsListAPiView, DeliveryCreateAPIView, VideosView, OrderCreateAPIView

urlpatterns = [
    path('foods/list/', FoodsListAPiView.as_view()),
    path('delivery/save/', DeliveryCreateAPIView.as_view()),
    path('videos/list/', VideosView.as_view()),
    path('videos/order/', OrderCreateAPIView.as_view())
]



