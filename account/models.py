from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")
        
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.is_admin=is_admin
        user.save(using=self._db)
        return user
    

    def create_superuser(self, email, username, password):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            is_admin=True
        )

        # user.is_admin=True
        user.is_staff=True
        user.is_active = True
        user.is_superuser=True
        user.is_deactivated = False


        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(max_length=255, unique=True, verbose_name="email")
    username = models.CharField(max_length=30, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_deactivated = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    
    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True