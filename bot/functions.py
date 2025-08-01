# import os
#
# from aiogram.fsm.state import StatesGroup, State
# from asgiref.sync import sync_to_async
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
#
# # 2. Django ni ishga tushirish
# import django
#
# django.setup()
# from apps.models import TelegramUser, QRCode
#
# from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
#
#
# @sync_to_async
# def save_user(**kwargs):
#     query = TelegramUser.objects.filter(user_id=kwargs['user_id'])
#     if not query.exists():
#         TelegramUser.objects.create(**kwargs)
#
#
# @sync_to_async
# def check_code(code):
#     query = QRCode.objects.filter(code=code)
#     if query.exists():
#         return False
#     else:
#         return True
#
#
# class States(StatesGroup):
#     first_name = State()
#     last_name = State()
#     phone_number = State()
