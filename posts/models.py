from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserLike(models.Model):
    pass
class UserComment(models.Model):
    pass

class UserPost(models.Model):

    user =models.ForeignKey(to=User,on_delete=models.CASCADE, related_name="post")
    title = models.CharField(max_length=200,editable=True,help_text="200 charectors only allowed.",blank=True,null=False,default="")
    post= models.TextField(max_length=500, editable=True, help_text="500 charectors only allowed.")
    post_image = models.ImageField(upload_to="Posts/",editable=True,blank=True,null=True)
    likes = models.ManyToManyField(to=UserLike,editable=True, blank=True)
    comments = models.ManyToManyField(to=UserComment,editable=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False, editable=False)
  