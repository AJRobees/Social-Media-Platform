from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth import forms
from django.forms.models import ModelForm

from django.core.exceptions import ValidationError

from .models import Profile

'''     All forms that related to User and Profile models. Each form class have the fields that only need to 
get the data from user. The automated fields are handled by the django itself without interaction with
user. '''

class RegisterForm(forms.UserCreationForm):
    class Meta:
        model = User
        fields = ["username","email","password1","password2" ]

class LoginForm(forms.AuthenticationForm):
    class Meta:
        fields = ["username","password"]

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ["username","email"]

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]          # 'excule' mean except this fields

    # In this "ProfileUpdateForm", it validates the date of birth 
        # DoB shouldn't be today,
        # Age must be below 100
        # Underage 17 is not allowed.
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        today = date.today()

        birth_year =(today.year - dob.year)*365
        birth_month = (today.month - dob.month)*30
        age = (birth_year + birth_month)//365

        print("dob",dob)
        print("today",today)
        
        # Check if date is in the future
        if dob > today:
            raise ValidationError('Date of birth cannot be in the future.')

        # Check if age is over 100 years
        if age > 100:
            raise ValidationError('Please enter a valid date of birth.')
        
        if age < 17:
            raise ValidationError('User is under 16 years old.')
        

        return dob


class PasswordUpdateForm(forms.PasswordChangeForm):
    # It get the password, authenticate it and validate it before pass to save. 
    class Meta:
        model = User
        fields = ["password"]

