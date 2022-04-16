from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['fullname','id','email','password']

@admin.register(Follow)
class AdminFollow(admin.ModelAdmin):
    list_display = ['who', 'follows_whom']