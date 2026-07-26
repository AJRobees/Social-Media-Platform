from django.db import models
from django.contrib.auth.models import User

# Profile models is here.

class GenderChoice(models.TextChoices):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
    PNS = "PNS"

class Profile(models.Model):
    
    user = models.OneToOneField(to=User,on_delete=models.CASCADE,related_name= "profile")
    profile_picture = models.ImageField(editable= True,upload_to="Profile pictures/",
                                        default="default_profile.png")
    bio = models.TextField(max_length= 255, editable= True, blank=True)
    gender =models.CharField(max_length=3,choices=GenderChoice.choices,default=GenderChoice.PNS, editable=True,blank=True)
    date_of_birth = models.DateField(editable= True, blank=True,null=True)
    phone_number = models.CharField(max_length=15,editable= True,help_text= "Enter contact number", blank=True)
    location = models.CharField(max_length=50,help_text= "Enter your location", blank=True)
    website = models.URLField(max_length=255, editable=True, blank=True)
    is_private = models.BooleanField(editable=True,default=False)

    def __str__(self):
        return f"{self.user} (Private: {self.is_private})"
