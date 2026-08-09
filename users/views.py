from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .form import *


# @login_required is an authenticaion protocol, it check whether the user is logged in or not.
# If the user is have't logged, redirects it to the login page


@login_required(login_url="login")
def profile(request):             # To get the current user's details

    ''' When the profile has been requested, it runs the authentication before allows it. 
     This function assign the requested user as the current user and pass it to the templete. '''
        
    user = request.user           # To get the current user's details

    return render(request,template_name="users/profile.html",context={"current_user":user})

@login_required(login_url="login")
def editProfile(request):     

    ''' After the user authentication, the requested user and user's date_of_birth is collected from the database
    and When the value is available in database for DoB then it converts the DoB into HTML supported date format before 
    pass the value along with the user to the templete. '''
       
    if request.method == "POST":               #   request.POST have the edited data to store in the database.

        '''  Both forms assigned with seperate model, "UserUpdateForm" connected with the django built-in user model 
         and "ProfileUpdateForm" connected with the Profile model to save the data got from the user.
          
           Before saving the data, checks validation and has_changed. Based on condition satisfaction the message will be
        shown.
          "p_form" have the parameter named files(request.FILES) and "u_form" is not because profile have the img on it and the 
        user given img will be passed under the files. It need the file to update the profile.  '''
        u_form = UserUpdateForm(data=request.POST,instance= request.user)  
        p_form = ProfileUpdateForm(request.POST,files=request.FILES,instance= request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():        # valids the form
            if u_form.has_changed() or p_form.has_changed():  # checks whether the data has been modified then saves the form
                u_form.save()
                p_form.save()

                messages.success(request=request,message="Details modified!")
                return redirect (to="home")
            
            messages.info(request=request,message="No changes made.")
            return redirect (to="home")
        
        messages.warning(request=request,message="Given data is invalid, check again!")
        return redirect (to="profile")
    
    user = request.user
    birth_date = (request.user.profile.date_of_birth)

    if birth_date is None:
        return render(request,template_name="users/edit_profile.html",context={"current_user":user})
    
    dob = date.isoformat(request.user.profile.date_of_birth)   # converts the date_of_birth into isoformat
    return render(request,template_name="users/edit_profile.html",context={"current_user":user,"dob":dob})

@login_required(login_url="login")
def home_page(request):                      # Renders the home page in the browser

        ''' The function is left empty because the home page needs to show the posts from the user friends.
        But the friends app is not been implemented for now, check it out in future for update.'''

        return render(request,template_name="home.html")


def registerUser(request):                 #  Registering the new user in the Database.

    '''  It checks whether the user is authenticated or anonymous user. If the authenticated user visits the
    register, redirect to home.
        When it is a anonymous user, the registeration form will be displayed to create the new user. The form
    will be goes for validation before creating new user.'''

    if request.user.is_authenticated:        # Redirect logged-in users to home page
        return redirect(to="home")
    
    else:
        if request.method == "POST":               #   request.POST haves the data of the new user to save in the database.
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request=request,message="User has been created.")
                return redirect (to="login")
            messages.info(request=request,message="Invalid Data!")
            return redirect (to="register")
      
        form = RegisterForm()
        return render(request,"users/register.html",{"form":form})


def loginPage(request):

    '''  It checks whether the user is authenticated or anonymous user. If the authenticated user visits the
    register, redirect to home.
        When it is a anonymous user, the login form will be displayed to login the user. It validates the user,
            if the user is valid then the authentication of the email and password will begin.
        
        the authorized user only able to login and redirected to home.'''

    if request.user.is_authenticated:           # Redirect logged-in users to home page
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
def logoutUser(request):             # Logout the user, then redirect to login page.
    logout(request)
    return redirect("login")
