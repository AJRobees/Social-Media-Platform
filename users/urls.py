from django.urls import path
from . import views

'''      Navigate the urls from the browser to get the information by directing the 
path where it want to be, constructs the urls according to the request received.'''

urlpatterns = [
    path("", views.home_page, name="home"),                          # 'home' or 'index' page where the site starts
    path("profile/", views.profile, name="profile"),                 # Navigate to user profile page
    path("edit_profile/", views.editProfile, name="edit_profile"),   # Leads to edit profile
    path("register/",views.registerUser,name="register"),            # To register the New user
    path("login/",views.loginPage,name="login"),                     # To login the user
    path("logout/",views.logoutUser,name="logout"),                  # To logout the user

]