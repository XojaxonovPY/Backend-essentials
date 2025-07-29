from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer, CharField

from DjangoAPI.settings import redis
from apps.models import Category, Product, Foods, Delivery, Order, User
import json


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'price')

    def create(self, validated_data):
        category = validated_data.get('category')
        category.product_count = category.product_count + 1
        category.save()
        return validated_data


class QRCodeSerializer(Serializer):
    data = CharField()


class FoodsModelSerializer(ModelSerializer):
    class Meta:
        model = Foods
        fields = '__all__'


class DeliverModelSerializer(ModelSerializer):
    class Meta:
        model = Delivery
        fields = ('id', 'foods', 'user', 'address')
        read_only_fields = ('id', 'user')


class OrderModelSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'videos', 'user')
        read_only_fields = ('id', 'user')


class UserPhoneNumberModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'phone_number', 'password')

    def validate_phone_number(self, value):
        query = User.objects.filter(phone_number=value)
        if query.exists():
            raise ValidationError('Phone number already exists')
        return value

    def validate_password(self, value):
        return make_password(value)


class UserEmailModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'email', 'password')

    def validate_email(self, value):
        query = User.objects.filter(email=value)
        if query.exists():
            raise ValidationError('Email already exists')
        return value

    def validate_password(self, value):
        return make_password(value)


class VerifyCodeSerializer(Serializer):
    pk = CharField(required=True)
    code = CharField(required=True)

    def validate(self, attrs):
        pk = attrs.get('pk')
        code = attrs.get('code')
        redis_data = redis.get(pk)
        if not redis_data:
            raise ValidationError('Code not found')
        data = json.loads(redis_data)
        code = data.get('code')
        if code != code:
            raise ValidationError('Verification code is invalid')
        self.user = data.get('user')
        self.pk=pk
        return attrs


# serializers.py
from rest_framework import serializers

class QuestionSerializer(serializers.Serializer):
    question = serializers.CharField()

