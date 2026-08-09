from django.contrib import admin
from django.urls import path,include
from .models import Profile

# Registers the Profile model in the admin.
admin.site.register(Profile)
