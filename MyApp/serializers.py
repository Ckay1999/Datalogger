from rest_framework_mongoengine import serializers,fields as field
from rest_framework import fields
from .models import Admin
from .models import Operator
from .models import Channel,User,UserOperator


class AdminSerializer(serializers.DocumentSerializer):
    user_id = fields.CharField(required=True)
    password = fields.CharField(required=False)
    email = fields.EmailField(required = False)
    phone = fields.IntegerField(required=False)
    class Meta:
        model = Admin
        fields = '__all__'

class OperatorSerializer(serializers.DocumentSerializer):
    user_id = fields.CharField(required=True)
    password = fields.CharField(required=False)
    email = fields.EmailField(required=False)
    phone = fields.IntegerField(required=False)
    department =fields.CharField(required=True)
    class Meta:
        model = Operator
        fields = '__all__'

class ChannelSerializer(serializers.DocumentSerializer):
    name = fields.CharField(required=True)
    unit = fields.CharField(required=True)
    minimum = fields.IntegerField(required=True)
    maximum = fields.IntegerField(required=True)

    class Meta:
        model = Channel
        fields = '__all__'

class UserSerializer(serializers.EmbeddedDocumentSerializer):
    channel_name=fields.CharField(required=True)

    class Meta:
        model = User
        fields = '__all__'

class UserOperatorSerializer(serializers.DocumentSerializer):
    user_id = fields.CharField(required=True)
    password =fields.CharField(required=False)
    email = fields.EmailField(required=False)
    phone =fields.IntegerField(required=False)
    department =fields.CharField(required=False)
    channel=UserSerializer(required=False)

    class Meta:
        model=UserOperator
        fields='__all__'
