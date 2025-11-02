import uuid
from io import BytesIO

import docker
import qrcode
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from DjangoAPI.settings import API_KEY, API_URL
from apps.models import Category, Product, QRCode
from apps.serializers import CategoryModelSerializer, ProductModelSerializer
from apps.serializers import QRCodeSerializer, QuestionSerializer, AutobotSerializer


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


@extend_schema(tags=["QR Code"])
class GenerateQRCodeGenericAPIView(GenericAPIView):
    serializer_class = QRCodeSerializer

    def get(self, request):
        token = str(uuid.uuid4())
        QRCode.objects.create(code=token)
        redirect_url = f'https://t.me/python_project_v1_bot?start={token}'
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(redirect_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        upload_url = "https://upload.uploadcare.com/base/"
        files = {'file': (f'{token}.png', buffer, 'image/png')}
        data = {
            'UPLOADCARE_PUB_KEY': settings.UPLOADCARE_PUBLIC_KEY,
            'UPLOADCARE_STORE': '1'
        }
        response = requests.post(upload_url, files=files, data=data)
        result = response.json()
        file_uuid = result.get('file')
        file_url = f"https://6vmpr9xieg.ucarecd.net/{file_uuid}/-/preview/"
        return Response({
            "qr_code_url": file_url,
            "redirect_url": redirect_url,
            "token": token
        })


@extend_schema(tags=['Web scraping'])
class WebGetAPIView(APIView):
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
class SeleniumAPIView(APIView):
    def get(self, request):
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        option.add_argument('--incognito')
        option.add_argument('--ignore-certificate-errors')
        option.add_argument('window-size=1000,800')
        option.add_argument('--disable-cache')
        option.add_argument('--disable-blink-features=AutomationControlled')
        option.add_argument('--user-agent=Selenium')
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=option)

        driver.get('https://uzum.uz/uz/category/hafta-tovarlari--895')
        wait = WebDriverWait(driver, 15, poll_frequency=1)
        products_path = (By.XPATH, "//a[contains(@class, 'product-card')]")
        cards = wait.until(EC.presence_of_all_elements_located(products_path))
        products = []
        for card in cards:
            title = card.find_element(By.XPATH, "//div[@class='product-card__title']").text
            by_card_price = card.find_element(By.XPATH, "//span[@class='currency']").text
            price = card.find_element(By.XPATH, "//span[contains(@class, 'card-price__regular')]").text

            products.append({
                "title": title,
                "by_card_price": by_card_price,
                "price": price
            })
        return Response(products)


@extend_schema(tags=["ChatBot"])
class AskGPTGenericAPIView(GenericAPIView):
    serializer_class = QuestionSerializer

    def post(self, request):
        headers = {"Authorization": f"Bearer {API_KEY}"}
        user_question = request.data.get('question')
        if not user_question:
            return Response({"error": "Savol kerak"}, status=400)
        payload = {
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": [
                {"role": "system", "content": "Siz foydalanuvchiga yordam beruvchi assistentsiz"},
                {"role": "system", "content": "Javoblar toliq o'zbek tilida bolishi kerak"},
                {"role": "user", "content": user_question}
            ]
        }
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                result = response.json()["choices"][0]["message"]["content"]
                return Response({"reply": result})
            else:
                return Response({
                    "error": f"API xatosi: {response.status_code}",
                    "detail": response.text
                }, status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


@extend_schema(tags=["Create Bot"])
class AutoBotGenericAPIView(GenericAPIView):
    serializer_class = AutobotSerializer

    def post(self, request):
        bot_token = request.data.get('bot_token')
        name = request.data.get('name')
        client = docker.from_env()
        container_name = f'{name}_con'  # oxirgi 5 belgidan container nomi
        try:
            container = client.containers.run(
                image=name,  # oldindan build qilingan image
                name=container_name,
                environment={"BOT_TOKEN": bot_token},
                detach=True
            )
            return Response({"message": "Bot ishga tushirildi", "container_id": container.id})
        except docker.errors.APIError as e:
            return Response({"error": str(e)}, status=500)
