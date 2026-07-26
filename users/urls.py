from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.editProfile, name="edit_profile"),
    path("register/",views.registerUser,name="register"),
    path("login/",views.loginPage,name="login"),
    path("logout/",views.logoutUser,name="logout"),


]