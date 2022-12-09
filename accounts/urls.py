from django.urls import path,re_path,include
from .views import *

app_name='accounts'

urlpatterns = [
    re_path(r'^validate_phone/',ValidatePhoneSendOTP.as_view()),
    re_path(r"^validate_otp/$",ValidateOTP.as_view()),
    re_path(r'^password/$',Password.as_view()),
    re_path(r'^validate_email', ValidateEmail.as_view()),
    re_path(r"^email_otp/$", ValidateOTPEmail.as_view()),
    re_path(r"^reset/$", EmailPasswordReset.as_view()),


]

