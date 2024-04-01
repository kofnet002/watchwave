from django.contrib import admin
from .models import User


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active',
                    'is_deactivated', 'is_staff', 'is_superuser', 'date_joined', 'last_login')


admin.site.register(User, CustomUserAdmin)