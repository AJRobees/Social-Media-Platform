from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .form import *


# @login_required is an authenticaion protocol, it check whether the user is logged in or not.
# If the user is have't logged, redirects it to the login page


@login_required(login_url="login")
def profile(request):             # To get the current user's details

    user = request.user           # To get the current user's details

    return render(request,template_name="users/profile.html",context={"current_user":user})

@login_required(login_url="login")
def editProfile(request):             
              
    if request.method == "POST":               #   request.POST haves the edited data to store in the database.
        
        u_form = UserUpdateForm(data=request.POST,instance= request.user)
        p_form = ProfileUpdateForm(request.POST,files=request.FILES,instance= request.user.profile)
        #pass_form = PasswordUpdateForm(request,request.POST)

          
        if u_form.is_valid() and p_form.is_valid():
            if u_form.has_changed() or p_form.has_changed():
                u_form.save()
                p_form.save()
                #pass_form.save()
                messages.success(request=request,message="Details modified!")
                return redirect (to="home")
            
            messages.info(request=request,message="No changes made.")
        messages.warning(request=request,message="Given data is invalid, check again!")
        return redirect (to="profile")
     
    user = request.user
    birth_date = (request.user.profile.date_of_birth)

    if birth_date is None:
        return render(request,template_name="users/edit_profile.html",context={"current_user":user})
    
    dob = date.isoformat(request.user.profile.date_of_birth)
    return render(request,template_name="users/edit_profile.html",context={"current_user":user,"dob":dob})

@login_required(login_url="login")
def home_page(request):                      # Renders the home page in the browser
    
    return render(request,template_name="home.html")


def registerUser(request):                 #  Registering the new user in the Database.

    if request.user.is_authenticated:        # Verifies, is the user is already logged in then redirect to Home page
        return redirect(to="home")
    
    else:
        if request.method == "POST":               #   request.POST haves the data of the new user to save in the database.
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect (to="login")
      
        form = RegisterForm()
        return render(request,"users/register.html",{"form":form})


def loginPage(request):
    if request.user.is_authenticated:           # Verifies, is the user is already logged in then redirect to Home page
        return redirect(to="home")
    
    else:
        if request.method == "POST":
            user = LoginForm(request,request.POST)

            # user stores the value from the authenticationForm,
            # If user is valid, the username and password are collects from the user object
            # veifies whether the username and password are authenticated one by comparing with the database
            # authenticate returns the user data or none, here it have two-step varification
            if user.is_valid():
                username = user.cleaned_data.get("username")
                password = user.cleaned_data.get("password")

                user = authenticate(request,username=username,password=password)

                if user is not None:
                    login(request, user)
                    return redirect (to="home",)
            
                else:
                    messages.info(request,message="Username or Password incorrect.")
            else:
                messages.info(request,message="Invalid Username or Password.")

        else:
            user =LoginForm()

        return render(request,template_name="users/loginPage.html",context={"user":user})

@login_required(login_url="login")
def logoutUser(request):             # To logout the user, then redirect into login page.
    logout(request)
    return redirect("login")
