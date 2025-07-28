import json
import random
import uuid

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from DjangoAPI.settings import redis
from apps.models import User
from apps.serializers import UserPhoneNumberModelSerializer, VerifyCodeSerializer, UserEmailModelSerializer
from apps.tasks import send_code_phone_number, send_code_email


@extend_schema(tags=['register'])
class RegisterPhoneNumberGenericAPIView(GenericAPIView):
    serializer_class = UserPhoneNumberModelSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        pk = str(uuid.uuid4())
        random_code = random.randrange(10 ** 5, 10 ** 6)
        send_code_phone_number.delay(user, random_code)
        redis.mset({pk: json.dumps({'user': user, 'code': random_code})})
        return Response({'message': 'Send verification code to phone_number', 'pk': pk}, status=status.HTTP_200_OK)


@extend_schema(tags=['register'])
class RegisterEmailGenericAPIView(GenericAPIView):
    serializer_class = UserEmailModelSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        pk = str(uuid.uuid4())
        random_code = random.randrange(10 ** 5, 10 ** 6)
        send_code_email.delay(user, random_code)
        redis.mset({pk: json.dumps({'user': user, 'code': random_code})})
        return Response({'message': 'Send verification code to email', 'pk': pk}, status=status.HTTP_200_OK)


@extend_schema(tags=['register'])
class VerifyCodeGenericAPIView(GenericAPIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.user
        user = User.objects.create(**data)
        user_serializer = None
        if user.phone_number:
            user_serializer = UserPhoneNumberModelSerializer(instance=user)
        if user.email:
            user_serializer = UserEmailModelSerializer(instance=user)
        redis.delete(serializer.pk)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=['login'])
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=['login'])
class CustomTokenRefreshView(TokenRefreshView):
    pass
