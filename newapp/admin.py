from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import CustomUser  # Import your custom user model here

admin.site.register(CustomUser)