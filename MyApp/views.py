from rest_framework_mongoengine import viewsets
from rest_framework import permissions
from MyApp.serializers import AdminSerializer,OperatorSerializer,ChannelSerializer,UserOperatorSerializer
from MyApp.models import Admin,Operator,Channel,UserOperator
from django.http import HttpResponse
from . import db
import requests
from rest_framework import permissions,status,generics
from rest_framework.response import Response
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import get_user_model
MyUser=get_user_model()

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/custom_password_reset_email.html'


def index(request):
    return HttpResponse('Success')


class AdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Admin to be viewed or edited.
    """
    lookup_field = 'id'
    serializer_class = AdminSerializer

    def get_queryset(self):
        return Admin.objects.all()

    def pre_save(self, obj):
        obj.file = self.request.FILES.get('file')

    def create(self,request,*args,**kwargs):
        super(viewsets.ModelViewSet,self).create(request,*args,**kwargs)
        user_id=request.data.get('user_id')
        password=request.data.get('password')
        phone=request.data.get('phone')
        email=request.data.get('email')

        MyUser.objects.create_superuser(user_id,email,phone, password)
        return Response({
            'status':True,
            'detail':'User created'
            })

class OperatorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Operator to be viewed or edited.
    """
    lookup_field = 'id'
    serializer_class = OperatorSerializer

    def get_queryset(self):
        return Operator.objects.all()

    def pre_save(self, obj):
        obj.file = self.request.FILES.get('file')

class ChannelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Channel to be viewed or edited.
    """
    lookup_field = 'id'
    serializer_class = ChannelSerializer

    def get_queryset(self):
        return Channel.objects.all()

    def pre_save(self, obj):
        obj.file = self.request.FILES.get('file')

    db.Master.month_hour()

class UserOperatorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Channel to be viewed or edited.
    """
    lookup_field = 'id'
    serializer_class = UserOperatorSerializer

    def get_queryset(self):
        return UserOperator.objects.all()

    def pre_save(self, obj):
        obj.file = self.request.FILES.get('file')

    permission_classes=(permissions.IsAuthenticatedOrReadOnly,permissions.IsAdminUser)
