from django.urls import path

from apps.views import *

urlpatterns = [
    path('login', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('register/phone_number/', RegisterPhoneNumberGenericAPIView.as_view()),
    path('register/email/', RegisterEmailGenericAPIView.as_view()),
    path('verify/code', VerifyCodeGenericAPIView.as_view())
]
