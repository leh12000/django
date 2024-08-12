from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomerManager(BaseUserManager):
    def create_user(self,username,email,first_name,last_name,phone=None,password=None):
        if not email:
            raise ValueError("email must not be none value")

        if not username:
            raise ValueError("username must not be none value")

        user=self.model(username=username,
                   email=self.normalize_email(email),
                   first_name=first_name,
                   last_name=last_name,
                   phone=phone
                   )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,email,first_name,last_name,phone,password=None):
        if not phone:
            raise ValueError("Phone number must be set")
        user=self.create_user(username,email,first_name,last_name,phone,password)

        user.is_admin=True
        user.is_superAdmin=True
        user.is_staff=True
        user.is_active=True

        user.save(using=self._db)
        return user


# Create your models here.
class Customer(AbstractBaseUser):
    username=models.CharField(max_length=100,unique=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=100)

    objects=CustomerManager()

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["username","first_name","last_name","phone"]

    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superAdmin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True

