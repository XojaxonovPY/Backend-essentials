from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import *

router = DefaultRouter()

router.register(r'categories', CategoryModelViewSet)
router.register(r'products', ProductModelViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('generic/code', GenerateQRCodeGenericAPIView.as_view()),
    path('get/news/', WebGetAPIView.as_view()),
    path('get/products/', SeleniumAPIView.as_view()),
    path('create/telegram/bot', AutoBotGenericAPIView.as_view()),
    path('ask/', AskGPTGenericAPIView.as_view())
]
