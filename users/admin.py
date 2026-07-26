from django.contrib import admin
from django.urls import path,include
from .models import Profile

# Models Registeration.
admin.site.register(Profile)
