from django.shortcuts import render
from rest_framework import permissions,status,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import PhoneOTP,EmailOTP
import random
import requests

from MyApp.serializers import AdminSerializer
from MyApp.models import Admin

from django.core.mail import send_mail
from datalogger.settings import EMAIL_HOST_USER

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.contrib.auth import get_user_model
MyUser=get_user_model()

class ValidateEmail(APIView):
    def post(self,request,*args,**kwargs):
        email=request.data.get('email')
        if email:

            user=Admin.objects.filter(email__iexact=  email)
            if not user:
                return Response({
                            'status':False,
                            'detail':'Users does not exists'
                            })
            else:
                otp_code=send_token(email)
                if otp_code:
                    old=EmailOTP.objects.filter(email__iexact = email)
                    if old.exists():
                        old=old.first()
                        count=old.count
                        if count>10:
                            return Response({
                                'status':False,
                                'detail':'Sending otp error. Limit exceeded. Please contact customer support'
                                })

                        old.count=count +1
                        old.save()
                        print("count increase",count)
                        return Response({
                            'status':True,
                            'detail':'Otp sent successfully at the mentioned email'
                            })

                    else:

                        EmailOTP.objects.create(
                            email=email,
                            otp=otp_code,
                            )
                        return Response({
                            'status':True,
                            'detail':'Otp sent successfully at the mentioned email'
                            })


                else:
                    return Response({
                        'status':False,
                        'detail':'Sending otp error'
                        })

        else:
            return Response({
                'status':False,
                'detail':'Email address is not given in post request'
                })


class ValidateOTPEmail(APIView):

    def post(self,request,*args,**kwargs):
        email=request.data.get('email',False)
        otp_sent=request.data.get('otp',False)

        if email and otp_sent:
            old=EmailOTP.objects.filter(email__iexact= email)
            if old.exists():
                old=old.first()
                otp=old.otp
                if str(otp_sent)==str(otp):
                    old.validated=True
                    old.save()
                    return Response({
                        'status':False,
                        'detail':'OTP matched.Please proceed to reset your password'
                        })
                else:
                    return Response({
                        'status':False,
                        'detail':'OTP Incorrect'
                        })

            else:
                return Response({
                    'status':False,
                    'detail':'First proceed via sending otp request'
                    })

        else:
            return Response({
                'status':False,
                'detail':'Please provide both email and otp for validation'
                })


class EmailPasswordReset(APIView):
    def post(self,request,*args,**kwargs):
        email=request.data.get('email',False)
        password=request.data.get('password',False)

        if email:
            old=EmailOTP.objects.filter(email__iexact= email)
            if old.exists():
                old=old.first()
                validated=old.validated


                if validated and MyUser.objects.filter(email=email).exists():
                    user=Admin.objects.get(email=email)
                    myuser=MyUser.objects.get(email=email)


                    if password:
                        user.password=password
                        myuser.set_password(password)

                        user.save()
                        myuser.save()
                        old.delete()

                        return Response({
                            'status':True,
                            'detail':'Password updated successfully'
                            })

                    else:
                        return Response({
                            'status':False,
                            'detail':'Please provide password'
                            })

                else:
                    return Response({
                        'status':False,
                        'detail':'Please verify otp first.'
                        })

            else:
                return Response({
                    'status':False,
                    'detail':'Please verify email address'
                    })

        else:
            return Response({
                'status':False,
                'detail':'Please provide email address'
                })




#____________________________________________________________
class ValidatePhoneSendOTP(APIView):

    def post(self,request,*args,**kwargs):
        phone_number=request.data.get('phone',False)
        if phone_number:
            phone=str(phone_number)
            user=Admin.objects.filter(phone__iexact= phone)
            if not user:
                return Response({
                            'status':False,
                            'detail':'Users does not exists'
                            })


            else:
                key=send_otp(phone)
                if key:
                    old=PhoneOTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        old=old.first()
                        count=old.count
                        if count>10:
                            return Response({
                                'status':False,
                                'detail':'Sending otp error. Limit exceeded. Please contact customer support'
                                })

                        old.count=count +1
                        old.save()
                        print("count increase",count)
                        return Response({
                            'status':True,
                            'detail':'Otp sent successfully'
                            })

                    else:

                        PhoneOTP.objects.create(
                            phone=phone,
                            otp=key,
                            )
                        return Response({
                            'status':True,
                            'detail':'Otp sent successfully'
                            })


                else:
                    return Response({
                        'status':False,
                        'detail':'Sending otp error'
                        })

        else:
            return Response({
                'status':False,
                'detail':'Phone number is not given in post request'
                })




class ValidateOTP(APIView):

    def post(self,request,*args,**kwargs):
        phone=request.data.get('phone',False)
        otp_sent=request.data.get('otp',False)

        if phone and otp_sent:
            old=PhoneOTP.objects.filter(phone__iexact= phone)
            if old.exists():
                old=old.first()
                otp=old.otp
                if str(otp_sent)==str(otp):
                    old.validated=True
                    old.save()
                    return Response({
                        'status':False,
                        'detail':'OTP matched.Please proceed to reset your password'
                        })
                else:
                    return Response({
                        'status':False,
                        'detail':'OTP Incorrect'
                        })

            else:
                return Response({
                    'status':False,
                    'detail':'First proceed via sending otp request'
                    })

        else:
            return Response({
                'status':False,
                'detail':'Please provide both phone and otp for validation'
                })



class Password(APIView):
    def post(self,request,*args,**kwargs):
        phone=request.data.get('phone',False)
        password=request.data.get('password',False)

        if phone:
            old=PhoneOTP.objects.filter(phone__iexact= phone)
            if old.exists():
                old=old.first()
                validated=old.validated


                if validated and MyUser.objects.filter(phone=phone).exists():
                    user=Admin.objects.get(phone=phone)
                    myuser=MyUser.objects.get(phone=phone)


                    if password:
                        user.password=password
                        myuser.set_password(password)
                        myuser.save()
                        user.save()
                        old.delete()

                        return Response({
                            'status':True,
                            'detail':'Password updated successfully'
                            })

                    else:
                        return Response({
                            'status':False,
                            'detail':'Please provide password'
                            })

                else:
                    return Response({
                        'status':False,
                        'detail':'Please verify otp first.'
                        })

            else:
                return Response({
                    'status':False,
                    'detail':'Please verify phone first'
                    })

        else:
            return Response({
                'status':False,
                'detail':'Please provide phone number'
                })


def send_otp(phone):
    if phone:
        key= random.randint(99999,999999)
        name='django_user'
        link=f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=7d7c6a75-a72e-11ea-9fa5-0200cd936042&to={phone}&from=CHAHAT&templatename=verification&var1={name}&var2={key}'
        requests.get(link)
        print(key)
        return key
    else:
        return False


def send_token(email):
    if email:
        otp1=random.randint(99999,999999)
        subject="Reset Your Password"
        msg='Your one time password is '+str(otp1)

        send_mail(subject,msg,EMAIL_HOST_USER,[email],fail_silently=False)
        return otp1
    else:
        return False
