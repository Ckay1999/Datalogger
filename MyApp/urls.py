from django.urls import include, re_path
from rest_framework import routers
from . import views
from . import broker
from .views import CustomPasswordResetView

from MyApp.apiviews import UserOperatorDetail
router = routers.DefaultRouter()
router.register(r'admin_data', views.AdminViewSet,basename='Admin')
router.register(r'operator_data', views.OperatorViewSet,basename='Operator')
router.register(r'channel_data', views.ChannelViewSet,basename='Channel')
router.register(r'user_data', views.UserOperatorViewSet,basename='User')

urlpatterns = [
    re_path('', include(router.urls)),
    re_path(r'^index',views.index,name='index'),

    re_path(r'^oper/$',UserOperatorDetail.as_view()),
    re_path(r'^oper/(?P<pk>[a-zA-Z0-9-]+)/$', UserOperatorDetail.as_view()),


]

broker.client.loop_start()

