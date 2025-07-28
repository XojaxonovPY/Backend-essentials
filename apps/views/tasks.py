import os
import uuid
from datetime import datetime

from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from apps.models import Category, Product, QRCode
from apps.serializers import CategoryModelSerializer, ProductModelSerializer, QRCodeSerializer

import qrcode
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@extend_schema(tags=['tasks'])
class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    http_method_names = ['post']


@extend_schema(tags=['tasks'])
class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    http_method_names = ['post']


@extend_schema(
    request=QRCodeSerializer,  # Swagger'ga inputni ko‘rsat
    responses={200: dict},  # Javob turi
    tags=["QR Code"]  # Swagger'da guruhlash
)
class GenerateQRCodeView(APIView):
    def get(self, request):
        # 1. Unikal token yaratamiz
        token = str(uuid.uuid4())
        QRCode.objects.create(code=token)
        # 2. Telegram URL + token
        data = f'https://t.me/python_project_v1_bot?start={token}'

        # 3. QR code yaratish
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # 4. Faylni saqlash
        filename = f"qr_{datetime.now().strftime('%Y%m%d%H%M%S%f')}.png"
        path = os.path.join(settings.MEDIA_ROOT, 'qrcodes', filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        img.save(path)

        # 5. QR code rasm URL
        file_url = request.build_absolute_uri(settings.MEDIA_URL + f"qrcodes/{filename}")

        # 6. QR link va tokenni qaytarish
        return Response({
            "qr_code_url": file_url,
            "redirect_url": data,
            "token": token
        })


@extend_schema(tags=['Web scraping'])
class WebGet(APIView):
    def get(self, request):
        response = requests.get("https://kun.uz")
        html_code = response.text  # html

        soup = BeautifulSoup(html_code, "html.parser")
        news_list = []

        for i in soup.find_all('div', {'class': 'small-cards__default-item'}):
            news = {
                'title': i.find("a").text,
                'image': i.find("img")['src']
            }
            news_list.append(news)
        return Response(news_list)


@extend_schema(tags=['Web scraping'])
class SeleniumView(APIView):
    def get(self, request):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        driver.get('https://uzum.uz/uz/category/hafta-tovarlari--895')
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card")))

        cards = driver.find_elements(By.CSS_SELECTOR, ".product-card")
        products = []

        for card in cards:
            title = card.find_element(By.CSS_SELECTOR, '.product-card__title').text
            price = card.find_element(By.CSS_SELECTOR, '[data-test-id="product-card__actual-price"]').text

            products.append({
                "title": title,
                "price": price
            })
        driver.quit()
        return Response(products)
