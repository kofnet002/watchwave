from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")
        
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, email, username, password):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )

        user.is_admin=True
        user.is_staff=True
        user.is_active=True
        user.is_superuser=True

        user.save(using=self._db)
        return user
    
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=100)
    is_deactivated = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username