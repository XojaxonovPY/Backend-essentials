from django.core.mail import send_mail

from DjangoAPI.settings import EMAIL, PASSWORD, EMAIL_HOST_USER
import requests

from celery import shared_task


@shared_task
def send_code_phone_number(user: dict, code):
    response = requests.post('https://notify.eskiz.uz/api/auth/login', json={
        "email": EMAIL,
        "password": PASSWORD
    })
    token = response.json().get('data').get('token')
    token_type = response.json().get('token_type')
    message = 'Bu Eskiz dan test'
    # message=code
    sms = requests.post(
        'https://notify.eskiz.uz/api/message/sms/send',
        headers={"Authorization": f"{token_type.title()} {token}"},
        data={
            "mobile_phone": user.get('phone_number'),
            "message": message,
            "from": "8888",
            "callback_url": "http://0000.uz/test.php"
        }
    )
    print(sms.json())
    return f'Success:{code}'


@shared_task
def send_code_email(user: dict, code):
    send_mail(
        subject='!Tasdiqlash kodingiz!',
        message=f'Sizning tasdiqlash kodingiz:{code}',
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.get('email')],
        fail_silently=False,
    )
    return 'Success'
