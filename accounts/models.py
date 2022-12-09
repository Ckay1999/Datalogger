from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, user_id,email,phone,password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not user_id:
            raise ValueError('Users must have a User id')

        if not password:
            raise ValueError('Users must have password')

        user = self.model(
            user_id=user_id,
            email=email,
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id,email,phone, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            user_id,
            email,
            phone,
            password=password,
        )
        user.admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    user_id=models.CharField(unique=True,max_length=250)
    phone=models.IntegerField()
    email = models.EmailField()
    first_login=models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['phone','email']

    def __str__(self):
        return self.user_id

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.admin

    @property
    def is_admin(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.admin

    @property
    def is_active(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.active

class PhoneOTP(models.Model):
    phone_regex=RegexValidator(regex =r'^\+?1?\d{9,14}$',message="Phone must be entered in the format: '+999999999'. Up to 14 digits allowed.")

    phone=models.CharField(validators=[phone_regex], max_length=17, unique=True)
    otp=models.CharField(max_length=9,blank=True,null=True)
    count=models.IntegerField(default=0,help_text='Number of otp sent')
    validated=models.BooleanField(default=False,help_text='If it is true, that means user have validated otp correctly in second API')

    def __str__(self):
        return str(self.phone)+' is sent '+str(self.otp)


class EmailOTP(models.Model):

    email=models.EmailField( max_length=255, unique=True)
    otp=models.CharField(max_length=9,blank=True,null=True)
    count=models.IntegerField(default=0,help_text='Number of otp sent')
    validated=models.BooleanField(default=False,help_text='If it is true, that means user have validated otp correctly in second API')

    def __str__(self):
        return str(self.email)+' is sent '+str(self.otp)
