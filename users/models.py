from django.db import models
from django.contrib.auth.models import User

'''  In here, the Profile model is linked with with the django built-in user model through the
one to one field. It allow the user to have one profile at a time if want new then have to create 
new user or edit this one.

"profile_picture" will save or load the image from the "Profile pictures/" in media directory.

"GenderChoice" class is an helper class that contains the options for the User gender.  '''

class GenderChoice(models.TextChoices):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
    PNS = "PNS"        # PNS - Prefer Not to Say (default)

class Profile(models.Model):
    
    user = models.OneToOneField(to=User,on_delete=models.CASCADE,related_name= "profile") # Adding 1 to 1 relation
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
