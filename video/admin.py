from django.contrib import admin
from .models import Video


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'updated_at')



admin.site.register(Video, CustomUserAdmin)