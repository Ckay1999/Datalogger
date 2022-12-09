from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import PhoneOTP,EmailOTP
from .forms import UserChangeForm,UserCreationForm
admin.site.register(PhoneOTP)
admin.site.register(EmailOTP)

from django.contrib.auth import get_user_model
MyUser=get_user_model()

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('user_id','phone','email', 'admin')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('user_id', 'password')}),
        ('Personal info', {'fields': ('phone','email')}),
        ('Permissions', {'fields': ('admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id','email', 'phone', 'password1', 'password2'),
        }),
    )
    search_fields = ('user_id',)
    ordering = ('user_id',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
