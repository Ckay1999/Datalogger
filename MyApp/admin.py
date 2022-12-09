from django_mongoengine import mongo_admin as admin

from .models import Admin
from .models import Operator
from .models import Channel,User,UserOperator

class UserOperatorAdmin(admin.DocumentAdmin):
    model=UserOperator
    fields='__all__'

#admin.site.register(Operator,OperatorAdmin)
admin.site.register(Admin)
admin.site.register(Operator)
admin.site.register(Channel)

