from django.forms import models

from .models import UserPost

class CreatePostForm(models.ModelForm):
    class Meta:
        model = UserPost
        fields = ["title","post","post_image"]

class EditPostForm(models.ModelForm):
    class Meta:
        model = UserPost
        fields = ["title","post","post_image"]

        
        