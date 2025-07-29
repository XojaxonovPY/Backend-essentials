from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import CategoryModelViewSet, ProductModelViewSet, GenerateQRCodeView, WebGet, SeleniumView, AskGPTView

router = DefaultRouter()

router.register(r'categories', CategoryModelViewSet)
router.register(r'products', ProductModelViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('generic/code', GenerateQRCodeView.as_view()),
    path('get/news/', WebGet.as_view()),
    path('get/products/', SeleniumView.as_view()),

]
urlpatterns += [
    path('ask/', AskGPTView.as_view()),
]
