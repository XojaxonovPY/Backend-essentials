from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import Model, CharField, DecimalField, BigIntegerField, IntegerField
from django.db.models import SET_NULL, ForeignKey
from pyuploadcare.dj.models import ImageField, FileField

class Category(Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = CharField(max_length=255)
    product_count = IntegerField(default=0)

    def __str__(self):
        return self.name


class TelegramUser(Model):
    user_id = BigIntegerField()
    first_name = CharField(max_length=255, null=True, blank=True)
    last_name = CharField(max_length=255, null=True, blank=True)
    phone_number = CharField(max_length=255, null=True, blank=True)
    username = CharField(max_length=255, null=True, blank=True)


class Product(Model):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=9, decimal_places=2)
    category = ForeignKey(Category, on_delete=SET_NULL, null=True, blank=True, related_name='products')


# ==============================================QRcode========================================

class QRCode(Model):
    code = CharField(max_length=255)


# ==============================================Delivery========================================


class Foods(Model):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=9, decimal_places=2)
    quantity = IntegerField(default=0)


class Delivery(Model):
    foods = ForeignKey('apps.Foods', on_delete=SET_NULL, null=True, blank=True, related_name='deliveries')
    user = ForeignKey('apps.User', on_delete=SET_NULL, null=True, blank=True, related_name='deliveries')
    address = CharField(max_length=255)


class Videos(Model):
    name = CharField(max_length=255)
    video = FileField(blank=True,null=True)
    price = DecimalField(max_digits=9, decimal_places=2)


class Order(Model):
    user = ForeignKey('apps.User', on_delete=SET_NULL, null=True)
    videos = ForeignKey('apps.Videos', on_delete=SET_NULL, null=True)


class CustomUserManager(UserManager):
    def _create_user_object(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone_number must be set")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, phone_number, password, **extra_fields):
        user = self._create_user_object(phone_number, password, **extra_fields)
        user.save(using=self._db)
        return user

    async def _acreate_user(self, phone_number, password, **extra_fields):
        user = self._create_user_object(phone_number, password, **extra_fields)
        await user.asave(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)

    create_superuser.alters_data = True


class User(AbstractUser):
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    phone_number = CharField(max_length=255, unique=True, null=True, blank=True)
    username = None
    objects = CustomUserManager()
