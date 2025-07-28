from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Foods, Videos
from apps.serializers import FoodsModelSerializer, DeliverModelSerializer, OrderModelSerializer


@extend_schema(tags=['delivery'])
class FoodsListAPiView(ListAPIView):
    queryset = Foods.objects.all()
    serializer_class = FoodsModelSerializer


@extend_schema(tags=['delivery'])
class DeliveryCreateAPIView(CreateAPIView):
    serializer_class = DeliverModelSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['videos'])
class VideosView(APIView):
    def get(self, request):
        videos = Videos.objects.all()
        urls = []
        for i in videos:
            url = {
                'name': i.name,
                'url': request.build_absolute_uri(i.video.url)
            }
            urls.append(url)
        return Response(urls)


@extend_schema(tags=['videos'])
class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderModelSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
